#!/usr/bin/env python3
"""Interactive universal installer and exporter for Expert Panel."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import export_formats

RENDER_AGENTS = HERE / "render_host_agents.py"

INSTALLER_VERSION = "27.3.0"
SKILL_DIR = "expert-panel"
MARKER = ".expert-panel-install.json"
SKIP = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}

TARGETS = {
    "generic": (".agents/skills", "Agent Skills generic"),
    "claude-code": (".claude/skills", "Claude Code"),
    "codex": (".agents/skills", "Codex / Agent Skills"),
    "opencode": (".config/opencode/skills", "OpenCode"),
    "gemini-cli": (".gemini/skills", "Gemini CLI"),
    "openclaw": (".openclaw/workspace/skills", "OpenClaw"),
    "hermes": (".hermes/skills", "Hermes"),
    "custom": ("", "Custom path"),
}

WINDOWS_RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}

def safe_name(name: str) -> bool:
    if not name or "\\" in name or name.startswith("/") or len(name) > 4096:
        return False
    parts = name.split("/")
    if any(p in {"", ".", ".."} or len(p) > 255 or ":" in p or p.endswith((" ", ".")) for p in parts):
        return False
    if any(p.split(".", 1)[0].casefold() in WINDOWS_RESERVED for p in parts):
        return False
    return True

def find_payload_root(explicit: str | None = None) -> Path:
    candidates = [
        explicit,
        os.environ.get("EXPERT_PANEL_SOURCE"),
        HERE.parent / "skills" / SKILL_DIR,
        HERE.parent / SKILL_DIR,
        Path.cwd() / "skills" / SKILL_DIR,
        Path.cwd() / SKILL_DIR,
        Path.cwd()
    ]
    for c in candidates:
        if not c:
            continue
        p = Path(c).expanduser().resolve()
        if (p / "SKILL.md").is_file():
            return p
        if (p / "skills" / SKILL_DIR / "SKILL.md").is_file():
            return p / "skills" / SKILL_DIR
    raise FileNotFoundError("Cannot locate canonical skills/expert-panel/SKILL.md payload")

def default_root(kind: str) -> Path:
    rel, _ = TARGETS[kind]
    if not rel:
        raise ValueError(f"target {kind} requires an explicit destination path")
    return Path.home() / rel

def target_path(kind: str, dest: str | None) -> Path:
    if kind == "custom" and not dest:
        raise ValueError("custom target requires --dest")
    root = Path(dest).expanduser() if dest else default_root(kind)
    root = root.resolve()
    return root if root.name == SKILL_DIR else root / SKILL_DIR

def install_subagents(source: Path, agents_dest: Path, agent_format: str, ru: bool = False) -> dict[str, object]:
    if agents_dest.exists() and any(agents_dest.iterdir()):
        raise FileExistsError(f"{'Папка сабагентов не пуста' if ru else 'Subagent destination is not empty'}: {agents_dest}")
    agents_dest.mkdir(parents=True, exist_ok=True)
    if agent_format == "json":
        copied = []
        for agent in sorted((source / "agents").glob("expert-*.json")):
            target = agents_dest / agent.name
            shutil.copy2(agent, target)
            copied.append(target)
    elif agent_format in {"md", "markdown"}:
        import subprocess
        host = "opencode" if "opencode" in str(agents_dest).casefold() else "claude-code"
        subprocess.run([sys.executable, str(RENDER_AGENTS), "--host", host, "--source", str(source), "--dest", str(agents_dest)], check=True)
        copied = sorted(agents_dest.glob("expert-*.md"))
    else:
        raise ValueError("agents format must be json or md")
    return {"format": "md" if agent_format == "markdown" else agent_format, "target": str(agents_dest), "files": [p.name for p in copied], "hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in copied}}


def install_agent(source: Path, target: Path, dry_run: bool, yes: bool, ru: bool = False) -> dict[str, object]:
    if target == source or source in target.parents:
        raise ValueError("Папка назначения не может быть внутри исходной папки" if ru else "Destination cannot be inside source")
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"{'Папка уже существует, перезапись запрещена' if ru else 'Refusing to overwrite existing destination'}: {target}")

    selected = [p for p in sorted(source.rglob("*")) if p.is_file() and not (set(p.relative_to(source).parts) & SKIP) and p.name != MARKER and p.suffix not in {".pyc", ".zip"}]
    files_map = {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in selected}
    info = {"installer": INSTALLER_VERSION, "skill": SKILL_DIR, "profile": "SOLO", "files": files_map, "target": str(target)}

    print(f"{'Источник' if ru else 'Source'}: {source}")
    print(f"{'Назначение' if ru else 'Target'}: {target}")
    print(f"{'Файлов' if ru else 'Files'}: {len(selected)}")
    if dry_run:
        return {"mode": "dry-run", **info}
    if not yes and (not sys.stdin.isatty() or input(f"{'Установить Expert Panel в' if ru else 'Install Expert Panel to'} {target}? [y/N]: ").strip().casefold() not in {"y", "yes", "д", "да"}):
        raise PermissionError("Установка отменена пользователем" if ru else "Installation cancelled")

    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir()
    for path in selected:
        rel = path.relative_to(source)
        out = target / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, out)

    (target / MARKER).write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"mode": "installed", **info}

def uninstall(target: Path, yes: bool, ru: bool = False) -> dict[str, object]:
    marker = target / MARKER
    if not target.is_dir() or not marker.is_file():
        raise ValueError("Папка не является проверенной установкой Expert Panel" if ru else "Destination is not a marked Expert Panel installation")
    try:
        info = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("Некорректный маркер установки" if ru else "Invalid install marker") from exc
    if info.get("skill") != SKILL_DIR or not info.get("files"):
        raise ValueError("Маркер не соответствует установщику" if ru else "Marker does not match installer")

    for rel, expected in info["files"].items():
        path = target / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"{'Файл изменён или отсутствует, удаление отменено' if ru else 'Modified or missing file, refusing uninstall'}: {rel}")
    agents_p = Path(info["agents_path"]) if info.get("agents_path") else None
    for rel, expected in info.get("agent_files", {}).items():
        path = agents_p / rel if agents_p else None
        if not path or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"{'Файл субагента изменён или отсутствует, удаление отменено' if ru else 'Modified or missing subagent, refusing uninstall'}: {rel}")

    plugin_p = Path(info["plugin_path"]) if "plugin_path" in info and info["plugin_path"] else None
    agents_p = Path(info["agents_path"]) if "agents_path" in info and info["agents_path"] else None

    prompt_details = [str(target)]
    if plugin_p and plugin_p.exists():
        prompt_details.append(f"{'плагин' if ru else 'plugin'}: {plugin_p}")
    if agents_p and agents_p.exists():
        prompt_details.append(f"{'субагенты' if ru else 'subagents'}: {agents_p}")

    details_str = " + ".join(prompt_details)
    confirm_msg = f"{'Удалить проверенную установку' if ru else 'Remove verified installation'} ({details_str})? [y/N]: "
    if not yes and (not sys.stdin.isatty() or input(confirm_msg).strip().casefold() not in {"y", "yes", "д", "да"}):
        raise PermissionError("Удаление отменено" if ru else "Uninstall cancelled")

    # 1. Remove subagents if recorded
    removed_agents = []
    if agents_p and agents_p.exists():
        for agent_file in info.get("agent_files", {}):
            af_path = agents_p / agent_file
            if af_path.is_file():
                af_path.unlink()
                removed_agents.append(agent_file)
        # If agents dir is empty, remove it
        try:
            if not any(agents_p.iterdir()):
                agents_p.rmdir()
        except OSError:
            pass

    # 2. Remove plugin if recorded
    removed_plugin = False
    if plugin_p and plugin_p.exists():
        shutil.rmtree(plugin_p)
        removed_plugin = True

    # 3. Remove skill directory
    shutil.rmtree(target)
    return {
        "mode": "uninstalled",
        "target": str(target),
        "plugin_removed": str(plugin_p) if removed_plugin else None,
        "agents_removed": removed_agents
    }

def _choose(prompt: str, options: list[str], ru: bool = False) -> int:
    print(prompt)
    for index, option in enumerate(options, 1):
        print(f" {index}. {option}")
    prompt_str = "Выбор: " if ru else "Selection: "
    value = input(prompt_str).strip()
    if not value.isdigit() or not 1 <= int(value) <= len(options):
        raise ValueError("Некорректный выбор" if ru else "Invalid selection")
    return int(value) - 1

def interactive_menu(source: Path, yes: bool, lang: str | None = None):
    if not lang:
        print("\nLanguage / Язык:")
        print(" 1. Русский")
        print(" 2. English")
        v = input("Choice / Выбор [1/2]: ").strip()
        lang = "en" if v == "2" else "ru"
        
    ru = (lang == "ru")
    title = "Expert Panel: Универсальный установщик" if ru else "Expert Panel: Universal Installer"
    print("\n" + "="*56)
    print(f" {title} (v{INSTALLER_VERSION})")
    print("="*56)

    main_options = [
        "ИИ-агенты (скилл, JSON/Markdown сабагенты или solo)" if ru else "AI Agents (skill, JSON/Markdown subagents, or solo)",
        "Веб-чаты (получить скилл: ZIP для скиллов, обычный ZIP или Markdown)" if ru else "Web AI (export web-skill ZIP, universal ZIP, or Markdown)",
        "Удалить установленный скилл" if ru else "Uninstall existing installation",
        "Выход" if ru else "Exit"
    ]
    prompt = "Главное меню:" if ru else "Main menu:"
    choice = _choose(prompt, main_options, ru)

    if choice == 3:
        print("До свидания." if ru else "Goodbye.")
        return 0

    elif choice == 0:
        # Category 1: AI Agents
        sub_options = [
            "Установить скилл и сабагентов (выбрать JSON или Markdown)" if ru else "Install skill and subagents (choose JSON or Markdown)",
            "Установить только скилл (solo)" if ru else "Install skill only (solo)",
            "Назад" if ru else "Back"
        ]
        sub_choice = _choose("Настройка для ИИ-агентов:" if ru else "AI Agent options:", sub_options, ru)
        if sub_choice == 2:
            return interactive_menu(source, yes, lang)
        elif sub_choice == 0:
            target_names = [k for k in TARGETS if k != "custom"] + ["custom"]
            t_choice = _choose("Выберите целевую платформу:" if ru else "Select target agent platform:", target_names, ru)
            kind = target_names[t_choice]
            custom_root = input("Корневая папка skills: " if ru else "Skills root directory: ").strip() if kind == "custom" else None
            target = target_path(kind, custom_root)
            res = install_agent(source, target, False, yes, ru)

            want_agents = input("Установить также сабагентов? [Y/n]: " if ru else "Also install subagents? [Y/n]: ").strip().lower() in ("", "y", "yes", "д", "да")
            if want_agents:
                fmt_idx = _choose("Формат сабагентов:" if ru else "Subagent format:", ["JSON", "Markdown"], ru)
                agent_format = ["json", "md"][fmt_idx]
                if kind == "opencode":
                    default_agents = Path.home() / ".config" / "opencode" / "agents"
                elif kind == "claude-code":
                    default_agents = Path.home() / ".claude" / "agents"
                else:
                    default_agents = target.parent.parent / "agents" if target.parent.name == "skills" else target.parent / "agents"
                agents_dest_str = input(f"Папка сабагентов (Enter = {default_agents}): " if ru else f"Subagents folder (Enter = {default_agents}): ").strip()
                agents_dest = Path(agents_dest_str).expanduser().resolve() if agents_dest_str else default_agents
                sub = install_subagents(source, agents_dest, agent_format, ru)
                marker_path = target / MARKER
                marker_data = json.loads(marker_path.read_text(encoding="utf-8"))
                marker_data["profile"] = "AGENTS"
                marker_data["agents_path"] = str(agents_dest)
                marker_data["agent_format"] = agent_format
                marker_data["agent_files"] = sub["hashes"]
                marker_path.write_text(json.dumps(marker_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                res["subagents_installed"] = sub
                print(f"{'Сабагенты установлены' if ru else 'Subagents installed'}: {agents_dest} ({len(sub['files'])} files, {agent_format})")

            print(json.dumps(res, ensure_ascii=False, indent=2))
        elif sub_choice == 1:
            target_names = [k for k in TARGETS if k != "custom"] + ["custom"]
            t_choice = _choose("Выберите целевую платформу:" if ru else "Select target agent platform:", target_names, ru)
            kind = target_names[t_choice]
            custom_root = input("Корневая папка skills: " if ru else "Skills root directory: ").strip() if kind == "custom" else None
            target = target_path(kind, custom_root)
            res = install_agent(source, target, False, yes, ru)
            res["profile"] = "SOLO"
            print(json.dumps(res, ensure_ascii=False, indent=2))

    elif choice == 1:
        # Category 2: Web AI
        web_options = [
            "ZIP для веб-интерфейсов с загрузкой скиллов (Claude.ai Custom Skills / ChatGPT)" if ru else "ZIP for web platforms with skill upload (Claude.ai / ChatGPT)",
            "Универсальный ZIP для обычных чатов (инструкции + база знаний)" if ru else "Universal ZIP for regular chats (instructions + knowledge base)",
            "Одиночный Markdown-файл (без архивов, для любого чата)" if ru else "Single-file Markdown prompt (no archives, for any chat)",
            "Назад" if ru else "Back"
        ]
        web_choice = _choose("Варианты для веб-чатов:" if ru else "Web AI delivery formats:", web_options, ru)
        if web_choice == 3:
            return interactive_menu(source, yes, lang)
        fmt = ["web-skill", "universal-zip", "universal-text"][web_choice]
        out_prompt = "Папка для сохранения файла (Enter = текущая): " if ru else "Output directory (Enter = current): "
        out_dir = input(out_prompt).strip() or "."
        out = export_formats.export_format(fmt, Path(out_dir))
        print(f"{'Файл создан' if ru else 'Exported'}: {out}")

    elif choice == 2:
        # Category 3: Uninstall
        dest_prompt = "Путь к папке установленного скилла (expert-panel): " if ru else "Path to installed expert-panel directory: "
        dest = input(dest_prompt).strip()
        res = uninstall(Path(dest), yes, ru)
        print(json.dumps(res, ensure_ascii=False, indent=2))

    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description="Expert Panel 4-in-1 universal installer and exporter.")
    parser.add_argument("--source", help="Path to skills/expert-panel payload")
    parser.add_argument("--format", choices=["agent", "web-skill", "universal-zip", "universal-text"], help="Directly export or install a specific format")
    parser.add_argument("--target", choices=sorted(TARGETS), default="generic", help="Target agent platform (used with --format agent)")
    parser.add_argument("--dest", help="Destination path for installation or output directory")
    parser.add_argument("--agents-dest", help="Destination directory to install subagents")
    parser.add_argument("--agents-format", choices=("json", "md"), default="json", help="Subagent manifest format")
    parser.add_argument("--uninstall", metavar="DIR", help="Uninstall marked installation at path")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--lang", choices=["ru", "en"], help="Installer language (ru or en)")
    args = parser.parse_args()

    source = find_payload_root(args.source)
    ru = (args.lang == "ru")

    if args.uninstall:
        res = uninstall(Path(args.uninstall).resolve(), args.yes, ru)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    if args.format:
        if args.format == "agent":
            target = target_path(args.target, args.dest)
            res = install_agent(source, target, args.dry_run, args.yes, ru)
            if args.agents_dest and not args.dry_run:
                sub = install_subagents(source, Path(args.agents_dest).expanduser().resolve(), args.agents_format, ru)
                res["subagents_installed"] = sub
            print(json.dumps(res, ensure_ascii=False, indent=2))
            return 0
        else:
            out_dir = Path(args.dest).resolve() if args.dest else Path.cwd()
            res = export_formats.export_format(args.format, out_dir)
            print(f"Exported {args.format} to: {res}")
            return 0

    # Non-interactive CLI flags for direct agent install backwards compatibility
    if args.dest and not args.format:
        target = target_path(args.target, args.dest)
        res = install_agent(source, target, args.dry_run, args.yes, ru)
        if args.agents_dest and not args.dry_run:
            res["subagents_installed"] = install_subagents(source, Path(args.agents_dest).expanduser().resolve(), args.agents_format, ru)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0

    return interactive_menu(source, args.yes, args.lang)

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, FileExistsError, PermissionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
