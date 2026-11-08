> For `methodweft help`, `methodweft help`, `помощь`, `справка` and other commands, dispatch via `help-and-commands.md` before asking for a language, idea or methodology. Displaying help never starts a route.

# Universal intake and step-by-step mentorship (v0.10.0)

## Required first-run dialogue: language → raw idea → user selects method

1. **Language first.** At first skill activation, unless the conversation already specifies a communication language, ask only `На каком языке общаться? / Which language should we use?`. Wait for the answer. If the initial message explicitly provides a language and the idea together, reuse both and skip redundant questions. Existing user preferences and context take precedence; never insist on answering again.
2. **Free-form idea/task second.** After language is known, invite `Опишите своими словами, что хотите создать, исправить или исследовать. Можно очень коротко; технические слова не нужны.` Accept raw ideas, unclear aspirations, links, examples, uploaded projects, existing work and `не знаю`; don't force a form, seven-field questionnaire or a multiple-choice entry point. If a task is already described, don't request it again.
3. **Classify privately, no automatic PRIMARY selection.** Identify deliverable (software, agent skill, notes, teaching material, automation, research, document, creative, other), starting state, constraints, user experience and obstacles from supplied evidence. Unknown optional details stay `UNKNOWN`. If the user has no idea, help them discover one with a few simple examples *before* methodology recommendations. Do minimal read-only exploration if needed to distinguish eligible routes; don't start route-specific build, modify files or claim a method was selected.
4. **Propose, don't decide.** Using `methodology-selection.md` and `methodology-catalog.md`, recommend **2–4 suitable methodologies** with short, beginner-friendly descriptions of **every** option, and a concrete reason it fits the user's idea. Optionally label ONE best-supported candidate `(рекомендуется)` (translate label to user language); no forced label on uncertainty. Show shortlist numbers **and** fixed letter codes. End with `Выберите номер или код. 0 / все / methodweft methods — полный список всех методик.` (translated as appropriate). **WAIT for the user's selection**. This is a selection step, NOT RFB STOP 1 or STOP 2.
5. **Full catalog on demand.** Accept `0`, `все`, `все методики`, `методики`, `methodweft methods`, `methodweft methods`, `all`, `list`, `?` even if the user asks before providing an idea. Display **all 30 methodologies** with readable summaries, fixed global numbers, codes and applicability from `methodology-catalog.md`. Do not hide unusual routes or show bare names. The user can reply with the current menu's number or any unambiguous code.
6. **Selection is the user's right.** Only the user may set PRIMARY, either by picking a code/number, previously explicitly choosing a method, or saying `выбери сам` / `choose for me` (then record `USER_DELEGATED` and explain the choice). An agent's `(рекомендуется)` is NOT authorization. If the method is ill-suited, explain the mismatch, suggest others, and ask whether to keep or switch; never override silently. Keep the selection over later turns and resumes until the user changes it. If the user explicitly asks for direct execution without a methodology menu, that is delegation, not silent choice.
7. **Begin chosen method.** Only after selection/delegation, do that route's next stage from the appropriate playbook. Avoid redundant STOP gates (only chosen RFB build mode has STOP 1/2 later); separately seek real permissions for risky external actions. Supporting PM / Anti Slop modules do not become alternate PRIMARY methodologies.

## Conversation-state examples

- New session, language unknown: ask for language only; after answer, ask for idea only if not yet supplied; after idea, shortlist 2–4 and wait.
- Language + idea supplied in one message: immediately offer shortlist; no repeated intake.
- User says `все` or `0`: show full numbered 30-method catalog and wait for selection; keep their original idea in context.
- User says `3`: map to **the most recently displayed menu**, not to an assumed global ID. User says `I` or `RFB`: use the exact fixed route code.
- User names a method at the outset: accept it if compatible; no forced menu; do not ask again.
- User delegates: choose and explain best supported method, start it; do not count delegation as RFB STOP 1.

## Entry-point adaptations

| Entry | First meaningful action | Do not do |
|---|---|---|
| Nothing / no idea | Explore goals, interests, audience/problems and 2–3 prompts to surface ideas; propose a few concrete directions if useful | Pretend the user chose a product domain |
| Vague aspiration | Elicit what improvement/result is desired; show examples and low-cost probes | Demand technical specifications |
| Reference/link | Inspect with tools or ask for accessible files; extract transferable patterns, license and differences | Treat the reference as a mandate to clone/copy it |
| Rough idea | Clarify problem, who benefits, success signal and smallest demonstrable deliverable | Over-engineer stack or documentation |
| Clear idea | Confirm scope and destination, propose feasible alternatives and route | Re-ask the entire discovery questionnaire |
| Existing project/material | Inventory and preserve existing work; diff requirements and establish the smallest change | Recreate from scratch or replace user files |
| Other / unclear | Ask for one example of a satisfactory result and classify provisionally | Reject because it is not software |

## Guidance contract — every method, every task

- Work as a coach **through completion**: explain *what* the next meaningful action is, *why* it matters, what the user can do, and the smallest verifiable next output. Adjust vocabulary/depth to experience; novices get plain language and runnable examples, advanced users get concise rationale and constraints.
- Show clear progress: `CURRENT STAGE → completed evidence/output → next action → waiting on user/tool?`. Keep a checkpoint/handoff for interrupted chats, but do not promise asynchronous work or invented file creation.
- For a newly initiated guided task with no selected method, offer 2–4 methodology choices and WAIT for the user to choose. After that, offer task-level approaches only when necessary; STOP 1 only in RFB build mode.
- When useful, prepare an appropriate brief/outline/spec and acceptance checks; do not require a separate STOP 2 except RFB build mode. A software/agent repository may need `AGENTS.md`; a course, document, research brief or fictional world does **not** automatically need it. Do not invent irrelevant file types.
- Execute ordinary in-scope work after the user selects/delegates the PRIMARY method and relevant tool permissions are available; only RFB build mode needs an explicit plan approval at STOP 2. Iterate in small portions with user feedback. For writing, revise sections; for research, audit evidence; for course, pilot exercises; for software, run tests; for creative work, check consistency. **Every route ends with a usable artifact + task-specific quality checks + proportionate usage documentation/handoff**, or an explicit evidence-based `BLOCKED/NO_BUILD/RESEARCH_ONLY` exit.
- For already-approved existing workflows, continue from the verified stage, not from the opening, and require renewed approval only when the new work materially changes scope, risk, platform or cost.

## Explicit opening example (translate to the selected language)

`На каком языке общаться?` → `Опишите свою идею или задачу своими словами.` → `Вот три подходящие методики: 1. G ... 2. D ... 3. F ... Выберите номер или код; 0 / все / methodweft methods — полный список.` → [user selects `G`] → begin G playbook. No hidden automatic selection, no RFB STOP before the menu.
## P2P-style complexity and mentoring addendum (v0.10.0)

Classify effort as SMALL/MEDIUM/LARGE/CRITICAL **only to size verification and mentoring**, never to select the method instead of the user. If the user is a beginner, explain what each shortlisted method will *produce*, using concrete words. If the language is known from the user's latest instruction, do not insert an artificial separate-language turn. A saved method is valid only for the same compatible goal; a materially new goal returns to choice. See `p2p-architecture-adaptation.md` and `execution-assurance.md`.
