# Task-scoped orchestration of roles and optional skills

This reference extends, but does not replace, the `SKILL.md` execution classes, `references/expert_roles.md`, `references/thinking_modes.md`, or `references/skill_composition.md`. Load only for cross-domain work or when deciding whether a specialized capability is genuinely needed. The catalog in `role_registry.md` is a selection aid, not an instruction to activate every role. Host execution follows `host_profiles.md`: use single-context sequential perspective passes in web chat and delegate to real subagents only when the host provides verified isolated worker tools. Both share the same scope, evidence, and safety rules.

## Route without theater

1. Capture the deliverable, user's language, success signal, constraints, exclusions, and action permissions. If the request is clear and narrow, perform it directly. Apply explicit `BRAINSTORM`, `CRITIQUE`, `DECISION`, `PRE_MORTEM`, or `LEARN` modes from `thinking_modes.md` without convening a full panel unless independent cross-domain review is requested. A beginner asking to learn may use `mentor_path.md` without convening a panel.
2. For a focused specialist task select one lead lens and, if necessary, one different failure lens. For genuinely independent, consequential trade-offs use the existing QUICK/STANDARD/DEEP panel contract; do not create duplicate consensus from several similar personas.
3. For each role, define its distinct question, permitted evidence/tools, expected output, and stop condition. Treat roles as analytical lenses unless separately executed; same-context passes are not independent agents. Start with independent claim cards only when the panel route warrants them.
4. Match evidence to claims: inspected file/line, source and date, actual test command and result, or explicitly marked assumption. Resolve implementation disputes with a narrow test, factual disputes with sources, and user-value disputes with a concise choice. Stop critique when no new material evidence or decision-changing objection appears.
5. Synthesize the usable result, not a staged conversation. Mention material disagreement and unverified claims. No role may grant itself authority to publish, spend, modify accounts, reveal data, or widen scope.

## Optional external skill dispatch

A role name may resemble a skill name (e.g., `python-pro`, `react-expert`, `nextjs-developer`, `security-audit`, `fact-checker`, `project-planner`, `beautify-github-readme`). Similarity is only a discovery hint. First confirm the exact skill is available and callable in this host; a donor folder, online listing, or file in another installation is not an activation signal. Follow host instructions governing relevant skills. Respect the explicit composition preflight already specified for `HUMANIZE` and `README_STUDIO`: hand over the specialist workflow once and do not replay its bundled fallback. If no positive signal exists, use the relevant in-project reference or direct reasoning; do not fabricate a tool call. If invocation fails, report that status briefly, then use a safe local fallback once.

Pass the specialist only the minimum authorized task packet: original objective, scoped files, constraints, intended deliverable, allowed operations, secret/data boundaries, and verification requirement. Keep independent reviewers read-only by default, assign non-overlapping file scopes to parallel writers, and verify merged work yourself. Do not send private files to external services just to enrich a role. A specialist output is a candidate artifact, not independent proof; validate tests, citations, and claims before final synthesis.

## Escalation and stop rules

- Use `legacy_review_protocol.md` only for a material conflict between existing behavior, proposed change, or outdated documentation—not as a ritual for every edit.
- Ask the user when a missing value or permission is genuinely decision-dependent; for ordinary reversible implementation choose a sensible local default and proceed.
- Stop when the agreed observable success criteria are met or a concrete blocker is reported. Do not loop through role rounds without new evidence.
- Report which processes/tools actually ran and which checks did not. A claim card, simulated peer review, and installed skill are three different things.
