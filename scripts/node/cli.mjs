#!/usr/bin/env node
import { createInterface } from 'node:readline';
import { stdin as input, stdout as output } from 'node:process';
import { homedir } from 'node:os';
import { access, mkdir, readFile, readdir, lstat, writeFile, rm, copyFile } from 'node:fs/promises';
import { dirname, join, resolve, relative, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import { spawn } from 'node:child_process';

const VERSION = '27.3.0';
const NAME = 'expert-panel';
const MARKER = '.expert-panel-install.json';
const TARGETS = {
  generic: join(homedir(), '.agents/skills'),
  'claude-code': join(homedir(), '.claude/skills'),
  codex: join(homedir(), '.agents/skills'),
  opencode: join(homedir(), '.config/opencode/skills'),
  'gemini-cli': join(homedir(), '.gemini/skills'),
  openclaw: join(homedir(), '.openclaw/workspace/skills'),
  hermes: join(homedir(), '.hermes/skills'),
};

let lineIterator = null;
let activeRl = null;
async function ask(query) {
  if (query) output.write(query);
  if (!lineIterator) {
    activeRl = createInterface({ input, crlfDelay: Infinity });
    lineIterator = activeRl[Symbol.asyncIterator]();
  }
  const next = await lineIterator.next();
  return next.done ? '' : next.value;
}

const sha = bytes => createHash('sha256').update(bytes).digest('hex');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i++) {
    const item = argv[i];
    if (['--yes', '--dry-run', '--uninstall', '--check', '--help'].includes(item)) args[item.slice(2)] = true;
    else if (item.startsWith('--')) args[item.slice(2)] = argv[++i];
  }
  return args;
}

async function findRepoRoot() {
  const here = dirname(fileURLToPath(import.meta.url));
  const candidates = [
    resolve(here, '../..'),
    process.cwd(),
    resolve(here, '../../..'),
  ];
  for (const c of candidates) {
    try {
      await access(join(c, 'skills', NAME, 'SKILL.md'));
      return c;
    } catch {}
  }
  return null;
}

async function findPayload(explicit) {
  const here = dirname(fileURLToPath(import.meta.url));
  const candidates = [
    explicit,
    process.env.EXPERT_PANEL_SOURCE,
    join(here, 'package-payload', 'skills', NAME),
    resolve(here, '../../skills', NAME),
    join(process.cwd(), 'skills', NAME),
    join(process.cwd(), NAME),
  ].filter(Boolean);
  for (const candidate of candidates) {
    const root = resolve(candidate);
    try {
      await access(join(root, 'SKILL.md'));
      return root;
    } catch {}
  }
  throw new Error('Bundled skills/expert-panel/SKILL.md not found; set EXPERT_PANEL_SOURCE or --source');
}

async function runPythonExport(formatName, outDir) {
  const repo = await findRepoRoot();
  const here = dirname(fileURLToPath(import.meta.url));
  const bundled = join(here, 'package-payload', 'export_formats.py');
  const script = repo ? join(repo, 'scripts', 'export_formats.py') : bundled;
  return new Promise((res, rej) => {
    const proc = spawn('python', [script, '--format', formatName, '--output', outDir], { stdio: 'inherit' });
    proc.on('close', code => {
      if (code === 0) res();
      else rej(new Error(`Python export failed with code ${code}`));
    });
  });
}

async function collectFiles(root, base = root, rows = []) {
  for (const entry of await readdir(root, { withFileTypes: true })) {
    if (['.git', '__pycache__', 'node_modules', 'dist', 'build'].includes(entry.name) || entry.name === MARKER) continue;
    const full = join(root, entry.name);
    const stat = await lstat(full);
    if (stat.isSymbolicLink()) throw new Error(`Refusing source symlink: ${relative(base, full)}`);
    if (stat.isDirectory()) await collectFiles(full, base, rows);
    else if (stat.isFile() && !['.pyc', '.zip'].includes(full.split('.').pop().toLowerCase())) {
      const bytes = await readFile(full);
      rows.push({ path: relative(base, full), bytes, sha256: sha(bytes) });
    }
  }
  return rows;
}

function targetPath(root) {
  const resolved = resolve(root);
  return resolved.endsWith(NAME) ? resolved : join(resolved, NAME);
}

async function install(source, root, { yes = false, dryRun = false, ru = false } = {}) {
  const dest = targetPath(root);
  if (dest === source || dest.startsWith(source + '/')) throw new Error(ru ? 'Папка назначения не может быть внутри источника' : 'Destination cannot be inside source');
  try { await lstat(dest); throw new Error(ru ? `Папка уже существует, перезапись запрещена: ${dest}` : `Refusing to overwrite existing target: ${dest}`); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  const files = await collectFiles(source);
  if (!files.some(file => file.path === 'SKILL.md')) throw new Error(ru ? 'Источник не является скиллом Expert Panel' : 'Source is not an Expert Panel skill payload');
  output.write(`${ru ? 'Источник' : 'Source'}: ${source}\n${ru ? 'Назначение' : 'Target'}: ${dest}\n${ru ? 'Файлов' : 'Files'}: ${files.length}\n`);
  if (dryRun) return { mode: 'dry-run', target: dest, count: files.length };
  if (!yes && (await ask(ru ? `Установить Expert Panel в ${dest}? [y/N]: ` : `Install Expert Panel to ${dest}? [y/N]: `)).trim().toLowerCase() !== 'y') return { mode: 'cancelled' };
  await mkdir(dirname(dest), { recursive: true });
  await mkdir(dest, { recursive: false });
  const manifest = { installer: VERSION, skill: NAME, files: Object.fromEntries(files.map(file => [file.path, file.sha256])) };
  try {
    for (const file of files) {
      const out = join(dest, file.path);
      await mkdir(dirname(out), { recursive: true });
      await writeFile(out, file.bytes, { flag: 'wx' });
    }
    await writeFile(join(dest, MARKER), JSON.stringify(manifest, null, 2) + '\n', { flag: 'wx' });
  } catch (error) {
    await rm(dest, { recursive: true, force: true });
    throw error;
  }
  return { mode: 'installed', target: dest, count: files.length };
}

async function uninstall(target, yes = false, ru = false) {
  const root = resolve(target);
  const markerPath = join(root, MARKER);
  const manifest = JSON.parse(await readFile(markerPath, 'utf8'));
  if (manifest.installer !== VERSION || manifest.skill !== NAME || !manifest.files) throw new Error(ru ? 'Некорректный маркер установки' : 'Unrecognized install marker');
  for (const [rel, expected] of Object.entries(manifest.files)) {
    if (isAbsolute(rel) || rel.split(/[\\/]/).includes('..')) throw new Error(ru ? 'Небезопасный путь в маркере' : 'Unsafe install manifest path');
    if (sha(await readFile(join(root, rel))) !== expected) throw new Error(ru ? `Файл изменён, удаление отменено: ${rel}` : `Modified or missing file, refusing uninstall: ${rel}`);
  }

  const pluginPath = manifest.plugin_path ? resolve(manifest.plugin_path) : null;
  const agentsPath = manifest.agents_path ? resolve(manifest.agents_path) : null;
  const details = [root];
  if (pluginPath) details.push((ru ? 'плагин: ' : 'plugin: ') + pluginPath);
  if (agentsPath) details.push((ru ? 'субагенты: ' : 'subagents: ') + agentsPath);

  const confirmMsg = ru ? `Удалить проверенную установку (${details.join(' + ')})? [y/N]: ` : `Remove verified installation (${details.join(' + ')})? [y/N]: `;
  if (!yes && (await ask(confirmMsg)).trim().toLowerCase() !== 'y') return { mode: 'cancelled' };

  const removedAgents = [];
  if (agentsPath && manifest.agent_files) {
    for (const af of Object.keys(manifest.agent_files)) {
      const p = join(agentsPath, af);
      try { await rm(p); removedAgents.push(af); } catch {}
    }
  }

  let removedPlugin = false;
  if (pluginPath) {
    try { await rm(pluginPath, { recursive: true, force: true }); removedPlugin = true; } catch {}
  }

  await rm(root, { recursive: true, force: false });
  return { mode: 'uninstalled', target: root, plugin_removed: removedPlugin ? pluginPath : null, agents_removed: removedAgents };
}

async function _choose(prompt, options, ru = false) {
  output.write(prompt + '\n');
  options.forEach((opt, i) => output.write(` ${i + 1}. ${opt}\n`));
  const v = await ask(ru ? 'Выбор: ' : 'Selection: ');
  const n = Number(v.trim());
  if (!Number.isInteger(n) || n < 1 || n > options.length) throw new Error(ru ? 'Некорректный выбор' : 'Invalid selection');
  return n - 1;
}

async function interactiveMenu(source, yes, lang = null) {
  if (!lang) {
    output.write('\nLanguage / Язык:\n 1. Русский\n 2. English\n');
    const v = (await ask('Choice / Выбор [1/2]: ')).trim();
    lang = (v === '2') ? 'en' : 'ru';
  }
  const ru = (lang === 'ru');

  output.write('\n======================================================\n');
  output.write(` ${ru ? 'Expert Panel: Универсальный установщик' : 'Expert Panel: Universal Installer'} (v${VERSION})\n`);
  output.write('======================================================\n');

  const mainOptions = [
    ru ? 'ИИ-агенты (установка скилла, субагентов или плагина)' : 'AI Agents (install skill, subagents, or client plugin)',
    ru ? 'Веб-чаты (получить скилл: ZIP для скиллов, обычный ZIP или Markdown)' : 'Web AI (export web-skill ZIP, universal ZIP, or Markdown)',
    ru ? 'Удалить установленный скилл' : 'Uninstall existing installation',
    ru ? 'Выход' : 'Exit'
  ];

  const prompt = ru ? 'Главное меню:' : 'Main menu:';
  const choice = await _choose(prompt, mainOptions, ru);

  if (choice === 3) {
    output.write(ru ? 'До свидания.\n' : 'Goodbye.\n');
    return;
  } else if (choice === 0) {
    // Category 1: AI Agents
    const subOptions = [
      ru ? 'Установить скилл в каталог агента (Claude Code, Codex, OpenCode и др.)' : 'Install skill into agent directory (Claude Code, Codex, OpenCode, etc.)',
      ru ? 'Установить плагин для клиента (OpenCode, Claude Code, Zed IDE)' : 'Install client plugin with subagents (OpenCode, Claude Code, Zed IDE)',
      ru ? 'Назад' : 'Back'
    ];
    const subChoice = await _choose(ru ? 'Настройка для ИИ-агентов:' : 'AI Agent options:', subOptions, ru);
    if (subChoice === 2) {
      return interactiveMenu(source, yes, lang);
    } else if (subChoice === 0) {
      const targets = [...Object.keys(TARGETS), 'custom'];
      const targetIdx = await _choose(ru ? 'Выберите целевую платформу:' : 'Select target agent platform:', targets, ru);
      const key = targets[targetIdx];
      const targetPathVal = key === 'custom' ? await ask(ru ? 'Корневая папка skills: ' : 'Skills root directory: ') : TARGETS[key];
      const res = await install(source, targetPathVal, { yes, ru });

      const wantAgents = (await ask(ru ? 'Установить также 6 субагентов? [Y/n]: ' : 'Also install the 6 subagents? [Y/n]: ')).trim().toLowerCase();
      if (['', 'y', 'yes', 'д', 'да'].includes(wantAgents)) {
        const defaultAgents = key === 'opencode' ? join(homedir(), '.config/opencode/agents') : key === 'claude-code' ? join(homedir(), '.claude/agents') : join(resolve(targetPathVal, '..'), 'agents');
        const customAgents = (await ask(ru ? `Папка субагентов (Enter = ${defaultAgents}): ` : `Subagents folder (Enter = ${defaultAgents}): `)).trim();
        const agentsDest = resolve(customAgents || defaultAgents);
        await mkdir(agentsDest, { recursive: true });
        const srcAgents = join(source, 'agents');
        const agentFiles = await readdir(srcAgents);
        const copied = [];
        for (const af of agentFiles) {
          if (af.endsWith('.json')) {
            await copyFile(join(srcAgents, af), join(agentsDest, af));
            copied.push(af);
          }
        }
        res.subagents = { target: agentsDest, count: copied.length };
        output.write((ru ? 'Субагенты установлены: ' : 'Subagents installed: ') + `${agentsDest} (${copied.length})\n`);
      }
      output.write(JSON.stringify(res, null, 2) + '\n');
    } else if (subChoice === 1) {
      const clients = ['opencode'];
      const clientIdx = await _choose(ru ? 'Выберите подтверждённый native plugin host:' : 'Select a verified native plugin host:', ['OpenCode (native plugin + Agent Skills + Markdown subagents)'], ru);
      const targetClient = clients[clientIdx];
      const repo = await findRepoRoot();
      const bundledPluginScript = join(dirname(fileURLToPath(import.meta.url)), 'package-payload', 'plugins', 'setup_plugin.py');
      const pluginScript = repo ? join(repo, 'scripts/plugins/setup_plugin.py') : bundledPluginScript;
      return new Promise((res, rej) => {
        const proc = spawn('python', [pluginScript, '--target', targetClient], { stdio: 'inherit' });
        proc.on('close', code => {
          if (code === 0) res();
          else rej(new Error(`Plugin installer failed with code ${code}`));
        });
      });
    }
  } else if (choice === 1) {
    // Category 2: Web AI
    const webOptions = [
      ru ? 'ZIP для веб-интерфейсов с загрузкой скиллов (Claude.ai Custom Skills / ChatGPT)' : 'ZIP for web platforms with skill upload (Claude.ai / ChatGPT)',
      ru ? 'Универсальный ZIP для обычных чатов (инструкции + база знаний)' : 'Universal ZIP for regular chats (instructions + knowledge base)',
      ru ? 'Одиночный Markdown-файл (без архивов, для любого чата)' : 'Single-file Markdown prompt (no archives, for any chat)',
      ru ? 'Назад' : 'Back'
    ];
    const webChoice = await _choose(ru ? 'Варианты для веб-чатов:' : 'Web AI delivery formats:', webOptions, ru);
    if (webChoice === 3) {
      return interactiveMenu(source, yes, lang);
    }
    const fmt = ['web-skill', 'universal-zip', 'universal-text'][webChoice];
    const promptMsg = ru ? 'Папка для сохранения файла (Enter = текущая): ' : 'Output directory (Enter = current): ';
    const out = (await ask(promptMsg)).trim() || '.';
    await runPythonExport(fmt, resolve(out));
    output.write((ru ? 'Файл создан: ' : 'Exported: ') + `${out}\n`);
  } else if (choice === 2) {
    // Category 3: Uninstall
    const destPrompt = ru ? 'Путь к папке установленного скилла (expert-panel): ' : 'Path to installed expert-panel directory: ';
    const dest = (await ask(destPrompt)).trim();
    const res = await uninstall(dest, yes, ru);
    output.write(JSON.stringify(res, null, 2) + '\n');
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    output.write(`npx expert-panel-installer [--format agent|web-skill|universal-zip|universal-text] [--target generic|claude-code|codex|opencode|gemini-cli|openclaw|hermes --dest ROOT] [--uninstall DIR] [--dry-run] [--yes] [--lang ru|en]\n`);
    return;
  }
  const source = await findPayload(args.source);
  const ru = (args.lang === 'ru');

  if (args.uninstall) {
    const res = await uninstall(args.uninstall, args.yes, ru);
    output.write(JSON.stringify(res, null, 2) + '\n');
    return;
  }

  if (args.plugin) {
    const repo = await findRepoRoot();
    const bundled = join(dirname(fileURLToPath(import.meta.url)), 'package-payload', 'plugins', 'setup_plugin.py');
    const script = repo ? join(repo, 'scripts/plugins/setup_plugin.py') : bundled;
    const commandArgs = [script, '--target', args.plugin];
    for (const [flag, value] of [['--skills-dest', args['skills-dest']], ['--agents-dest', args['agents-dest']], ['--plugin-dest', args['plugin-dest']]]) {
      if (value) commandArgs.push(flag, value);
    }
    if (args['dry-run']) commandArgs.push('--dry-run');
    if (args.yes) commandArgs.push('--yes');
    await new Promise((res, rej) => {
      const proc = spawn('python', commandArgs, { stdio: 'inherit' });
      proc.on('close', code => code === 0 ? res() : rej(new Error(`Plugin installer failed with code ${code}`)));
    });
    return;
  }

  if (args.format) {
    if (args.format === 'agent') {
      const dest = args.dest || TARGETS[args.target || 'generic'];
      const res = await install(source, dest, { yes: args.yes, dryRun: args['dry-run'], ru });
      if (args['agents-dest'] && !args['dry-run']) {
        const agentsDest = resolve(args['agents-dest']);
        await mkdir(agentsDest, { recursive: true });
        const srcAgents = join(source, 'agents');
        for (const af of await readdir(srcAgents)) {
          if (af.endsWith('.json')) await copyFile(join(srcAgents, af), join(agentsDest, af));
        }
      }
      output.write(JSON.stringify(res, null, 2) + '\n');
      return;
    } else {
      const outDir = args.dest ? resolve(args.dest) : process.cwd();
      await runPythonExport(args.format, outDir);
      return;
    }
  }

  if (args.dest && !args.format) {
    const dest = args.dest;
    const res = await install(source, dest, { yes: args.yes, dryRun: args['dry-run'], ru });
    output.write(JSON.stringify(res, null, 2) + '\n');
    return;
  }

  await interactiveMenu(source, args.yes, args.lang);
}

main().catch(error => { console.error(`Error: ${error.message}`); process.exitCode = 1; }).finally(() => { if (activeRl) activeRl.close(); });
