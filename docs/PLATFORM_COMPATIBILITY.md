# Platform compatibility

Expert Panel is designed to work at several capability levels. The workflow changes to fit the host instead of assuming that every AI has the same tools.

| Environment | Recommended form | What to expect |
| --- | --- | --- |
| OpenCode | Agent Skill under `~/.config/opencode/skills`, Markdown agents under `~/.config/opencode/agents`, optional native `.mjs` plugin under `~/.config/opencode/plugins/` | Native formats are supported; the plugin is an optional compaction/logging module, not a substitute for the skill or agents. |
| Claude Code | Skill under `~/.claude/skills`, Markdown subagents under `~/.claude/agents` | Claude Code's documented subagent format is Markdown with frontmatter; the OpenCode plugin is not installed here. |
| Codex / Gemini CLI / OpenClaw / Hermes | Agent Skill directory and host-specific agent mechanism when verified | Only the canonical skill is guaranteed; subagents require host-specific confirmation. |
| Zed | Agent Skill under `~/.agents/skills` or project `.agents/skills`, plus Zed MCP/tool settings | Zed's documented Agent Skills are native; the project does not claim a Zed plugin/subagent manifest. |
| Claude.ai / ChatGPT with custom Skills | Directory copy or export via installer | Native skill loading where supported by the account/workspace. |
| Ordinary web chat with attachments | `universal-zip` or `universal-text` | One model follows the portable system-role workflow without local subagents. |
| API or custom harness | `SKILL.md` plus selected references | Capabilities defined by the harness. |

## Capabilities that may vary

A host may or may not provide:

- native skill discovery;
- automatic use of several skills;
- file and repository access;
- web search;
- Python or shell execution;
- image or document rendering;
- separate subagents;
- persistent workspace storage.

Expert Panel uses a capability only when the host exposes it. Missing tools reduce automation, not the basic Markdown workflow.

## External specialist skills

Humanizer and Beautify GitHub README are optional enhancements. When a host explicitly loads or exposes one of them, Expert Panel can let that specialist handle the matching task. Otherwise the local fallback is used.

A portable attachment cannot normally discover or call another installed skill by itself.

## When only one model is available

The same model reviews the task in several focused passes. This can reveal different assumptions, but it is not the same as independent review by separate models or people. The final answer should describe it as review passes rather than independent agents.

## When web or file access is missing

- Without web access, current claims should be marked as not freshly verified.
- Without full file access, the review should describe which files or excerpts were actually inspected.
- Without code execution, automated tests should not be reported as run.

## Privacy-sensitive work

Prefer a local host when files should remain on the computer. In a web interface, the platform's privacy terms, workspace settings, and connector permissions still apply. Expert Panel does not bypass those controls.
