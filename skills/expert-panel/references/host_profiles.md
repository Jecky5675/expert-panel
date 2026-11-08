# Host execution profiles: web chat and agent delegation

Expert Panel has **one canonical core instruction set**. It does not maintain separate platform-specific skills. Use this reference to adapt execution to the host environment actually available.

## Profile 1: Web chat (single model, bounded perspectives)

Apply in ChatGPT, Claude.ai, Gemini, Perplexity, or any chat without verified isolated subagents. Attach or paste `portable/EXPERT_PANEL_BALANCED.md`, `portable/MENTOR_AND_PROJECT_REVIEW_STANDALONE.md`, or `portable/EXPERT_PANEL_LITE.md`.

- One model runs sequential perspective passes. It must not claim independent agents, external execution, or background processes.
- Each lens has a distinct question, evidence budget, and stop condition.
- First-pass cards are drafted before cross-comparison.
- Only conflicting or overlapping points are debated.
- Resolves facts by accessible evidence; values by user priority.
- Deliverable: single synthesized answer with findings, uncertainty, and next verifiable step.

## Profile 2: AI agents (real subagent delegation)

Apply in Claude Code, OpenCode, Codex, Gemini CLI, or custom harnesses with verified task/subagent tools.

- The parent agent coordinates, scopes, enforces boundaries, and validates evidence.
- Review roles are read-only by default. Assign minimal task packets with explicit non-goals, specific paths, permitted tools, and stop conditions.
- Parallelize only independent read-only investigations.
- If multiple writers are needed, assign strictly non-overlapping file scopes; the parent reconciles diffs and runs tests once.
- Subagents must not recruit further subagents recursively.
- If real isolation or task tools are absent, the agent must fall back to Profile 1 and state that limitation honestly.

## Common rules for both profiles

- **Two-layer roles:** built-in core roles (orchestrator, domain lens, evidence auditor, adversary, synthesizer) plus dynamic task-specific roles (stack, attack-surface, data, UI).
- **Capability resolution:** exact host skill first; bundled full module second; bundled compact fallback third; remote reference only with explicit permission.
- **Offensive security:** attacker modeling and exploitability validation require an owned or authorized target; indiscriminate targeting and destructive attacks are prohibited.
- **Permissions:** file creation, modification, network calls, and publication require appropriate host capability and user authorization.
