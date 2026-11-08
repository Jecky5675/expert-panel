# Beginner path: from free-form request to verified next step

Load only when the user is learning, asks for guided delivery, or cannot yet formulate a technical task. This compact Expert Panel route is supplemented by the attributed MIT snapshot in `vendor/methodweft/entry-and-mentoring.md`; consult that file only when more detailed beginner dialogue is useful, while this file and the root router remain controlling. For a clear ordinary request, do the work directly and explain the result. Do not turn every coding task into an intake interview, mandatory methodology menu, or mandatory panel.

## Entry

Accept a rough idea, a broken feature, an existing folder, or a question in the user's own words. Mirror the goal in one sentence and state only assumptions that affect the next step. Ask for missing information only if it changes what should be done and cannot be established from the available artifact. If a repository is available, inspect its actual structure before suggesting a stack, commands, or a rewrite. Explain jargon on first use, in the user's language, without talking down to them.

Choose proportional guidance:

- **Clear task:** perform the smallest authorized change; then show what changed, how it was checked, and what remains unverified.
- **Ambiguous objective with materially different paths:** offer two or three plainly worded approaches with a concrete trade-off and a recommended default when justified. Let the user choose if values, budget, or irreversible direction matter. If the user delegates the choice, choose and state the assumption.
- **Early idea or learner request:** propose a small observable milestone (for example, one user action working locally), then a short sequence of build → inspect → adjust. Prefer a reversible prototype over a long speculative specification.
- **High-risk or externally consequential action:** pause at the actual approval boundary, not at every research or planning step; obtain explicit authorization before publishing, spending, deleting data, changing accounts, or accessing third parties.

The user may change direction after seeing results. Re-evaluate from current evidence rather than treating an earlier option as a permanent contract. Do not copy MethodWeft route names, counts, command syntax, or special approval gates into this path; this project has its own routing and safety rules.

## Teaching loop

1. **Locate the task.** Name the user-visible outcome, present starting point, and the next action in ordinary language. A single-sentence question is enough if blocked.
2. **Work a small slice.** State what will be changed or demonstrated, then act within permissions. Give a short explanation of *why this step matters* where it aids learning; avoid narrating every keystroke.
3. **Check observable evidence.** Tie an acceptance criterion to an inspected artifact or actually run check. Label proposed checks, unavailable tools, and unrun tests honestly; never report imaginary progress.
4. **Invite a useful choice.** After a real result, offer a next small milestone or ask which user-facing direction to pursue only when the choice genuinely changes the work. Do not ask for approval of a routine reversible edit already requested.
5. **Repair and close.** If a check fails, explain the failure plainly, try a bounded fix, and report any remaining issue. Finish with a usable artifact or an exact blocker—not a ceremonial phase handoff.

A compact learner-facing result can be: **What works now → What I checked → What is still open → One sensible next step.** On larger tasks use `references/role_orchestration.md` for a task-scoped reviewer; on an actual older-code conflict use `references/legacy_review_protocol.md`. Neither reference is required for routine teaching.

## Boundaries

A beginner's uncertainty is not permission to infer files, run scripts, install packages, register skills, transmit data, or deploy. Distinguish examples from commands actually executed. A named “mentor” is an explanation style, not a separate person with hidden work. Avoid false assurances of security, completeness, and compatibility; expose uncertainty with an achievable way to verify it.
