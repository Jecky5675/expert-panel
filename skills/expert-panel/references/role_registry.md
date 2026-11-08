# Task-scoped role registry

Load this catalog only when selecting a new domain lens. `SKILL.md`, `references/expert_roles.md`, and `references/thinking_modes.md` remain the primary execution contracts; these are optional role cards, not mandatory seats. A role is a reasoning operation performed by the current assistant unless a separate process was actually invoked. Do not invent an employee, credential, lived experience, independent vote, tool access, or completed investigation. Pick one owner per deliverable, merge overlapping lenses, and stop when the task is answered. For routine requests, use no panel.

For each selected role record its question, evidence, uncertainty, and stop condition. A role's recommendation is not evidence; distinguish inspected artifacts, reproducible tests, sourced claims, and unverified inference. Verify time-sensitive claims against current primary material when available, or explicitly mark them unverified. Do not turn a skill name or donor directory into a claim that the skill is installed, active, licensed for reuse, or independently tested. Optional exact-skill dispatch follows `references/role_orchestration.md` and the existing `references/skill_composition.md`; no dispatch is necessary to apply a lens.

## Discovery and delivery

| Lens | Distinct operation / decision question | Evidence and expected output | Stop / boundary |
|---|---|---|---|
| Product / user advocate | Identify target user, problem, and smallest measurable outcome; is this feature useful? | User statement, observed workflow, constraints; explicit assumptions, success metric, smallest reversible slice. | Do not invent interviews, market demand, or approval. |
| Beginner mentor | Translate a free-form idea or unfamiliar repository into one achievable next step; what does the learner understand and want to do? | User's own words, visible files, prior attempts; plain-language options, tiny next action, feedback on observed results. | Do not force a methodology quiz or block an ordinary requested fix; use `mentor_path.md` only when guidance is useful. |
| Architect | Compare boundaries, dependencies, reversibility, and operating cost; what is the simplest maintainable shape? | Existing code/contracts, constraints, deployment assumptions; alternatives, decision rationale, migration seam. | Do not prescribe microservices or a rewrite by fashion. |
| Planning / delivery | Sequence dependencies and checkpoints; what can be validated first? | Scope, time/resources, blockers; a staged plan with acceptance signals and rollback when needed. | Do not present invented estimates as commitments. |
| Operations / reliability | Test deployability, observability, support load, and recovery; who maintains this after launch? | Existing environments, logs/runbooks if authorized, failure budgets; operational risks and recovery checks. | No deployment, account change, or external action without approval. |
| Documentation / README | Make the first successful action and limitations findable; what can a reader reproduce? | Inspected project commands/config, verified claims; concise audience-appropriate prose, working links/examples. | Do not fabricate badges, benchmarks, screenshots, or executed checks; use README_STUDIO route for visual README requests. |

## Implementation stack selectors

Select only the stack evident in the repository or requested by the user. If none is determined and the choice materially affects architecture, explain 2–3 viable options and ask; otherwise keep a small technology-neutral step. A stack selector does not imply an installed specialist skill.

| Lens | Distinct operation / decision question | Evidence and expected output | Stop / boundary |
|---|---|---|---|
| Python implementation | Trace runtime, packages, typing, and test seams; what is the smallest idiomatic change? | Python files, dependency manifest, relevant test output; localized patch and narrow test. | Do not assume package version or install dependencies silently. |
| C++ implementation | Inspect ownership, lifetimes, toolchain, ABI, and target standard; where could correctness or compatibility fail? | Build files, compiler settings, warnings/sanitizer output if actually run; minimal change and compile/test evidence. | Do not promise portability or memory safety without evidence. |
| C# / .NET implementation | Check framework target, nullable flow, async/disposal, and API compatibility; which contract must stay stable? | Project files, code, test result; focused implementation and compatibility notes. | Do not assume SDK, cloud account, or deployment access. |
| React implementation | Trace component state, rendering, and keyboard behavior; can the UI remain predictable and accessible? | Components/styles, running UI or tests when available; minimal UI change and interaction checks. | Do not claim visual/browser validation without seeing it. |
| Next.js implementation | Examine route/data boundaries, server/client split, caching, and framework version; what executes where? | Package/lockfile, route files, docs for confirmed version, test/build output; localized change. | Do not infer current API behavior from outdated examples. |

## Assurance and knowledge

| Lens | Distinct operation / decision question | Evidence and expected output | Stop / boundary |
|---|---|---|---|
| Offensive security / penetration testing | Think as the attacker: identify footholds, bypass controls, validate exploitability and connect demonstrated primitives into an attack chain; which trust boundary can an authorized tester actually cross? | Engagement scope, code/config, target-specific attack hypotheses, minimum-impact PoC in an authorized lab, exact observed result; attack narrative, preconditions, exploit status, fix and regression test. | Active testing requires owned/authorized scope. No indiscriminate targeting, destructive DoS, persistence beyond the test, real-user credential theft, supply-chain compromise or covert access against the owner. Load `offensive_security.md`. |
| UX / accessibility | Test user path, focus, semantics, contrast, responsive states; who is excluded by this design? | UI artifacts, user constraints, actual keyboard/browser checks if run; actionable failures and fixes. | Do not assert WCAG conformance from visual inspection alone. |
| QA / test | Turn acceptance criteria into observable examples; what regression would falsify success? | Existing tests, reproduction, commands and results; test gap, pass/fail/unrun clearly labeled. | Do not equate a proposed test with a passing test. |
| Research / fact-check | Separate primary evidence from repetition and inference; which claim survives source/date checks? | Citable independent sources, dates and contradictions; short evidence ledger and unresolved questions. | No invented citations or unsupported freshness claims. |
| Data / measurement | Define denominator, sampling, missingness, and causal limits; what can these data actually show? | Dataset provenance, schema, calculation or reproducible query; uncertainty and limitations. | Do not imply causation from correlation or expose private records. |
| Prompt / harness | Model instruction boundaries, tool permissions, evals, and failure containment; can the task be repeated safely? | Actual prompts/config, available tools, representative eval cases; copy-ready prompt or harness delta plus checks. | No fabricated model capabilities, hidden chain-of-thought, or safeguard evasion. |

| Compliance / ISMS & Privacy | Проверка регуляторных требований (GDPR/ISO 27001/HIPAA), прав субъектов данных, минимизации сбора и политик хранения; какие нормативные риски блокируют релиз? | Реестр данных, поток персональных данных, DPA/политики, конфигурация шифрования/доступа; реестр несоответствий и компенсирующие меры. | Не заменяет квалифицированную юридическую консультацию; не гарантирует сертификацию. |
| Database architect | Проверка схем данных, стратегий индексирования, нормализации/денормализации, миграций и транзакционных границ; выдержит ли схема целевую нагрузку? | DDL, схема миграций, профиль запросов, объёмы данных; схема с индексами, план миграции без простоя (expand/contract), оценка рисков блокировок. | Не заменять архитектурный анализ бенчмарками на искусственных синтетических данных. |
| Cloud-native / DevOps | Проверка контейнеризации, многоэтапной сборки, манифестов Kubernetes/IaC, сетевых политик и секретов; насколько воспроизводима и безопасна среда исполнения? | Dockerfile, compose/helm/k8s манифесты, CI/CD конфигурации; минимизированный образ (distroless), аудит привилегий контейнера, проверка уязвимостей базового образа. | Не применять избыточный Kubernetes для простых односерверных приложений. |
| Parity & migration testing | Обеспечение потиковой/побайтовой эквивалентности при переносе логики на новый стек/язык; как доказать, что поведение новой системы неотличимо от оригинала? | Запущенный оригинал как оракул, трейсы состояния по тикам, сценарии входов с фиксированным сидом; сравнительный отчет о расхождениях, детерминированные тесты. | Не полагаться на ручные юнит-тесты вместо потикового сравнения состояний оракула. |

## Visual and niche lenses

| Lens | Distinct operation / decision question | Evidence and expected output | Stop / boundary |
|---|---|---|---|
| SVG / visual design | Build a project-native, legible visual system; does the asset work at actual display sizes? | Brand artifacts and canvas constraints, inspected rendering if available; source asset and alt-text/motion considerations. | No copied donor assets; do not imply rendering or license clearance without checking. |
| Gaming / modding niche | Identify target game/version, mod API, asset permissions, and save compatibility; what can be changed safely? | Game/mod documentation and user-owned project files, platform/version and safe local test; compatibility caveats and backup/rollback. | No anti-cheat bypass, unauthorized account or asset access, or assumed compatibility. |

Cross-cutting control functions (orchestrator, evidence auditor, adversary, synthesizer) are defined in `references/expert_roles.md`. They are not extra biographies. Do not assemble the whole registry for a single task; choose genuinely different failure models and report only material disagreements.
