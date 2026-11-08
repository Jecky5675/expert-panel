# Installation

Expert Panel keeps one canonical payload at `skills/expert-panel/`. Install it interactively with the Node.js or Python package, or run the universal CLI directly from this repository. The installer places that same payload under the selected host's skill root; it does not generate platform-specific copies in the repository.

```bash
# From an npm registry release
npx expert-panel-installer

# From a PyPI release
pipx run expert-panel-installer

# From a cloned repository
node scripts/node/cli.mjs
python scripts/universal_installer.py
```

The interactive menu offers installation, single-file Markdown export, verified uninstall, or exit. `--dry-run` previews, `--yes` confirms; an existing target is never overwritten. A chat export is one portable Markdown file, not a native skill installation.

Common global roots are only defaults and may differ by workspace:

| Host family | Usual skills root |
|---|---|
| Generic/Codex-style Agent Skills | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| OpenCode | `~/.config/opencode/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| OpenClaw | `~/.openclaw/workspace/skills/` |
| Hermes | `~/.hermes/skills/` |

Non-interactive examples:

```bash
node scripts/node/cli.mjs --target generic --dry-run
node scripts/node/cli.mjs --target opencode --dest "$HOME/.config/opencode/skills" --yes
python -m expert_panel_installer.cli --target claude-code --dry-run
```

`--dest` is a skills root, not the final skill directory. The installer records hashes in an install marker and refuses modified or unmarked targets during uninstall. Reload hosts that scan skills only at startup.

### Agent role execution

Read `../skills/expert-panel/references/host_profiles.md`. Separate subagents are optional and must be real host processes/contexts. The parent assigns a distinct read-only question and narrow evidence scope to each reviewer, validates their evidence and owns the final answer. If isolation or a task tool is absent, use sequential lens passes and do not simulate independence.

## 4 Delivery Formats

Expert Panel provides **exactly 4 formats**:

1. **`agent`**: Native skill directory for AI agent hosts (Claude Code, Codex, OpenCode, Gemini CLI, OpenClaw, Hermes).
2. **`web-skill`**: Importable ZIP archive (`expert-panel-web-skill.zip`) for web platforms with custom skills support (Claude.ai Custom Skills, ChatGPT Workspace).
3. **`universal-zip`**: Chat ZIP archive (`expert-panel-universal-chat.zip`) containing `INSTRUCTIONS.md`, `HOW_TO_USE.md`, and `KNOWLEDGE.md` for chats with file attachments.
4. **`universal-text`**: Single self-contained Markdown prompt (`EXPERT_PANEL_INSTRUCTIONS.md`) for any chat without skill or ZIP attachment support.

## Web chats

Choose one of the 3 web delivery options:

- **If your chat supports uploading skill ZIP archives**: Choose format 2 (`web-skill`) in the installer.
- **If your chat supports attaching ZIP files**: Choose format 3 (`universal-zip`) in the installer. Attach the archive and tell the AI:
  ```text
  Read the attached archive and follow its Expert Panel instructions for my task.
  Task: [describe what you want to analyze, review, build, or audit]
  ```
- **If your chat accepts only text or single documents**: Choose format 4 (`universal-text`) in the installer. Paste the resulting text into custom instructions / system prompt, or attach it as a single `.md` file.

## API or custom harness

Use `skills/expert-panel/SKILL.md` as the entry and load references progressively. `scripts/panel_router.py` is the deterministic route. `scripts/role_orchestrator.py` returns built-in plus dynamic role cards; `scripts/skill_discovery.py` inventories exact host skills without running them. If the harness exposes isolated workers, use the agent-host profile in `skills/expert-panel/references/host_profiles.md`; otherwise use its web-chat profile.

## Optional verification

Python 3.10+ is not required to follow the Markdown method, but package maintainers should run:

```bash
python scripts/render_portable.py skills/expert-panel
python scripts/audit_release.py .
python scripts/validate_skill.py skills/expert-panel
python scripts/tests/run_evals.py skills/expert-panel
python scripts/role_orchestrator.py --check-cases
python scripts/tests/self_test.py skills/expert-panel
python -m compileall -q scripts
```

## Troubleshooting

| Symptom | Check |
|---|---|
| Skill not discovered | Verify the active skills root and `expert-panel/SKILL.md`; reload the host. |
| Installer refuses | It never overwrites. Move/rename the existing installation after reviewing it, or use another empty root. |
| Web chat claims subagents | Correct it to the web profile unless the platform exposed a verified isolated-worker API. |
| Complete file is too large | Use BALANCED, LITE or a standalone. |
| Donor module is present but does not run | Vendored files are optional instructions, not registered tools or dependency installation. |
| Tests are unavailable | Report NOT_RUN and use a concrete manual check; do not claim a pass. |
