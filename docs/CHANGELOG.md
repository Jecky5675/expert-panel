# Changelog

## 27.3.0 — 2026-11-08

- Integrated newly added donor skills from `claude-code-templates-main` and `game-parity-port-main`:
  - Added 3 new core practices to `practices_catalog.md`: `AD` (Parity Porting & Oracle Comparison), `AE` (Planning with Files / Manus-style 3-file memory pattern), and `AF` (Isolated Parallel Agent Dispatch). Updated total methodologies from 30 to 33.
  - Added 5 new dynamic specialist capability categories in `specialist_registry.json`: `parity_porting`, `compliance_isms_privacy`, `database_architecture`, `cloud_native_devops`, and `parallel_coordination`.
  - Added enterprise compliance, database architecture, and parity testing lenses to `role_registry.md`.
  - Added comprehensive practice cards in `donor_practice_cards.md` covering parity porting, session handoffs, compliance, parallel dispatch, database architecture, and cloud-native containers.
  - Updated `DONOR_INVENTORY.json`, `UPSTREAM_SOURCES.json`, `NOTICE.md`, and license records with MIT attribution for `claude-code-templates-main` and `game-parity-port-main`.

## 27.2.0 — 2026-10-26

- Added explicit `BRAINSTORM`, `CRITIQUE`, `DECISION`, `PRE_MORTEM`, and `LEARN` thinking modes with bilingual routing and informational-query safeguards.
- Added an attributed thinking-mode reference and compact evidence-first/TDD loop guidance; optional third-party quality tools are not required.
- Added local Vibe Security MCP integration guidance as independent concepts only; no unlicensed server code, policies, or patcher is bundled or executed.
- Added MIT license for original Expert Panel materials, with explicit carve-out for third-party materials and separate license notices.
- Refreshed donor review records and release instructions; public redistribution of unlicensed donor-derived material remains subject to rights review.

## 27.1.0 — 2026-10-26

- Rebuilt architecture as one canonical `expert-panel/` tree with a single universal installer (`scripts/universal_installer.py`) and Markdown exporter; eliminated duplicate platform folders, separate ZIP release packages, and unnecessary packaging clutter.
- Implemented two-layer roles: Layer 1 provides built-in control and domain functions; Layer 2 dynamically generates task-specific stack, attack-surface, data, or UI roles based on the user's request and confirmed artifacts.
- Reworked Security Review into an authorized offensive profile (`references/offensive_security.md`): models attacker footholds, control bypasses, minimum-impact exploit primitives, and attack chains for owned systems, labs, pentests, and CTFs.
- Added multi-tier skill discovery and orchestration (`scripts/skill_discovery.py`, `references/skill_orchestration.md`, `references/specialist_registry.json`): host-installed skill first, bundled full module second, bundled compact fallback third, remote reference fourth.
- Added first-class `BEGINNER_GUIDE` and `PROJECT_REVIEW` paths with attributed MIT snapshots for MethodWeft beginner guidance and Research First Builder decisions.
- Unified host-specific execution into `references/host_profiles.md`: sequential perspective passes for web chats and read-only subagent delegation for capable agent hosts.
- Retained unique legacy debate, audience, hypothesis, and detailed report capabilities; removed the legacy ethical/SCRIBE route and ethics personas/catalog entries by user request.

## 25.9.2 — 2026-08-06

- Added a shared safety-compatibility boundary that preserves benign objectives while redirecting unsafe mechanisms.
- Reworked Prompt Engineer to reject safeguard bypass, hidden-prompt extraction, secret exfiltration, unauthorized access, and harmful automation while keeping policy-compatible prompt optimization.
- Rebuilt Security Review as an authorized, defensive, read-only profile with secret redaction, safe local validation, no third-party scanning, and no live exploitation guidance.
- Reframed Humanizer as transparent style editing rather than authorship concealment or detector evasion; retained all 33 editorial patterns, locale handling, and no-fabrication rules.
- Updated portable editions, public documentation, metadata, regression checks, and deterministic package naming for the new boundary.
- Rewrote the main README in beginner-friendly Russian, removed maintainer-oriented publishing instructions, and made the quick-start path self-contained.

## 25.9.1 — 2026-08-04

- Re-synced the bundled Humanizer fallback from upstream [`blader/humanizer`](https://github.com/blader/humanizer) **v2.9.1** at `523374dee72d67c7b2b5f858ea0094ffda49c3ac`.
- Replaced adapted pattern wording with the upstream 33-pattern catalog body while keeping Expert Panel composition preflight, locale guardrails, and specialist routing.
- Strengthened the `HUMANIZE` specialist route: explicit lossless handoff to an installed `humanizer` skill when callable; single bundled fallback pass otherwise.
- Refreshed the third-party MIT license copy and upstream source notes for Humanizer.

## 25.9.0 — 2026-08-04

- Added a curated **knowledge-link base** (`knowledge/catalog.json` + `knowledge/INDEX.md`) so experts consult stable external sources by domain/tags instead of inventing citations.
- Added `references/knowledge_base.md` protocol: match domains, verify live targets when tools allow, cite `KB-…` ids in the evidence ledger, and never treat catalog membership as proof.
- Wired the knowledge base into `SKILL.md` core rules, evidence protocol, panel role setup, and specialist shared load map.
- Extended portable BALANCED/COMPLETE editions with the knowledge-base protocol; LITE notes the no-invention rule.
- Extended release audit allowlist and validator checks for `knowledge/` (HTTPS URLs, unique KB ids, minimum entry count).
- Added a twelfth deterministic self-test group covering the knowledge catalog.
- Clarified that the knowledge base is a link catalog, not an embedded document store or SQL database.

## 25.8.1 — 2026-07-30

- Removed the exact duplicate `portable/EXPERT_PANEL_COMPLETE.txt`; Markdown files are already plain UTF-8 text and work in plain-text interfaces.
- Removed the unused README workflow SVG, the code-of-conduct file, and GitHub issue/pull-request templates that were not required for skill execution or release verification.
- Kept validation scripts, evals, licenses, provenance, and maintainer documentation because they support reproducible public releases rather than runtime clutter.
- Changed P2P tracking to advisory mode: new P2P commits no longer fail the default upstream check.
- Made model catalogs, prices, token/context limits, provider availability, release dates, and vendor-specific settings explicitly ignored by default for P2P review.
- Expanded `.gitignore` for editor history, local work directories, patches, diffs, audit reports, and generated checksum files.

## 25.8.0 — 2026-07-30

- Rebuilt the README around a first-time user's questions: what the project is, how to start in one minute, which file to choose, and what each workflow does.
- Rewrote SECURITY.md as a factual release-verification summary with concrete checks, network behavior, limitations, and a simple reporting path.
- Simplified installation, platform, portable-use, architecture, contribution, release, issue, and pull-request documentation.
- Softened public-facing terminology while preserving the strict machine-facing runtime rules needed for safe, predictable execution.
- Confirmed the public `sanic732/P2P-4PDA-edition` repository and MIT license; added its license copy, exact reviewed revision, and methodology-only upstream tracking.
- Added a public-documentation regression test and updated the release baseline to 11 deterministic self-test groups.
- Refreshed README SVG copy so the visuals explain the workflow without requiring internal project terminology.

## 25.7.1 — 2026-07-29

- Audited the user-supplied P2P v8N.3 archive against the integrated coordination reference and documented which concepts were adapted without redistributing original files.
- Expanded `.gitignore` for credentials, local agent state, editor files, private datasets, local databases, reports, archives, and temporary artifacts.
- Added a deterministic public-release leak audit with a strict release-tree allowlist, dangerous-path checks, high-confidence secret signatures, local absolute-path detection, and size limits.
- Made the packager and GitHub Actions run the leak audit before packaging and again after clean extraction.
- Added deterministic tests proving that a fake private key, token, local path, forbidden agent file, and unknown top-level file block a release.
- Clarified that `.gitignore` is convenience only: it does not protect already tracked files and never replaces the release audit or manual review.

## 25.7.0 — 2026-07-29

- Re-reviewed every Python script, Markdown document, portable edition, public repository file, and release invariant from the v25.6.0 package.
- Reduced the root skill description to the stricter Claude web custom-skill limit while preserving Agent Skills discovery keywords.
- Reworked specialist composition into observable `EXPLICIT_CALL`, `AUTO_COMPOSED`, and `NO_POSITIVE_SIGNAL` states so web and local hosts do not pretend to discover or invoke unavailable skills.
- Fixed false-positive routing for informational security, prompt-engineering, Humanizer, README, upstream, and ordinary weather questions; expanded the bilingual suite to 54 cases.
- Hardened motion-spec validation against unsafe element IDs, duplicate IDs, invalid timing, zero-frame output, path-derived filenames, and input/output overwrite.
- Hardened README/SVG auditing with deeper URI decoding, HTML `srcset`, SMIL warnings, and README size preflight.
- Hardened eval loading, upstream checking, deterministic packaging, archive-member portability, and atomic portable generation.
- Added nine deterministic self-test groups, release-baseline validation, CI synchronization checks, and mutation coverage for the new invariants.
- Added a complete public GitHub surface: CI workflow, issue and PR templates, code of conduct, architecture, installation, platform compatibility, portable usage, and release documentation.
- Updated README guidance for native local agents, Claude.ai web, ChatGPT web, generic file-based chats, and API/custom harnesses without claiming capabilities the host has not exposed.

## 25.6.0 — 2026-07-29

- Added capability-based delegation to exact installed `humanizer` and `beautify-github-readme` skills, with lossless task packets and one-pass bundled fallback.
- Preserved self-contained portable behavior when native skill discovery or invocation is unavailable.
- Added method-diversity, non-obvious-option, anonymous peer-review, ensemble-baseline, theatrical-consensus, and multi-judge quality controls.
- Added router metadata and evals for preferred external skills.
- Added composition and deliberation references, validator invariants, and a dedicated self-test.
- Fixed duplicate changelog version headings and refreshed all generated portable editions.
- Re-reviewed similar open skills and current multi-agent deliberation research; retained capability-safe ideas while excluding vendor-specific orchestration.


## 25.5.1 — 2026-07-29

- Prepared the package for a public GitHub repository.
- Removed internal maintenance-agent and review-report artifacts from the release tree.
- Added `CONTRIBUTING.md`, `SECURITY.md`, `.gitignore`, and `.gitattributes`.
- Rewrote attribution and source-map language for public distribution without changing protected or third-party content.
- Updated validation to require the public repository documents and made standalone version self-tests metadata-driven.
- Preserved native and portable skill architectures, upstream pins, licenses, protected prompt checksum, and routing behavior.

- Fixed comparison over-triggering: generic value/string comparisons no longer activate PANEL; multi-criteria decisions still do.
- Added high-stakes decision-intent routing for financial, medical, legal, and similarly consequential recommendations.
- Updated `agents/openai.yaml` to a quoted, concise interface block whose default prompt explicitly invokes `$expert-panel`; removed the nonessential `policy` block.
- Made OpenAI metadata validation work without PyYAML and added exact release-command, standalone-version, portable-anchor, and provenance checks.
- Hardened README/SVG auditing against fenced-code false positives, HTML entities, repeated percent encoding, unsupported/absolute paths, CSS path escapes, DTD/entity parsing, and oversized SVGs.
- Added SVG security preflight and bounded width, duration, frame count, and size budgets before GIF rendering.
- Hardened deterministic ZIP timestamps and cross-platform member-name safety.
- Added six routing regressions and expanded mutation-style self-tests.
- Added superseding rules to the optional legacy expert catalog so stale years/personas cannot override current routing or evidence rules.
- Preserved the security prompt SHA-256, all 33 Humanizer patterns, upstream pins, and native/portable architecture.

## 25.4.0 — 2026-07-29

- Made multi-domain comparison/trade-off language participate in activation instead of appearing only in routing reasons.
- Expanded Humanizer trigger coverage for additional Russian and English naturalization phrases.
- Added five routing regressions and extended router self-tests.
- Preserved DIRECT/SPECIALIST/PANEL, payload-length neutrality, portable synchronization, and protected source invariants.

## 25.3.0 — 2026-07-29

- Added DIRECT/SPECIALIST/PANEL execution classes and removed payload length as a complexity trigger.
- Added first-class PROMPT_ENGINEER, SECURITY_REVIEW, RESEARCH, and UPSTREAM_MAINTENANCE routing.
- Added 28 routing evals, including long-payload and false-positive regressions.
- Added language/locale safeguards for Humanizer.
- Added BALANCED portable edition and PORTABLE_INDEX.
- Rewrote portable local links to stable in-file anchors and embedded reusable text templates.
- Strengthened README/SVG auditing with reference images, desc, URI normalization, DOCTYPE/ENTITY, active tags, CSS resources, JSON, and strict modes.
- Strengthened validation with exact version checks, direct-reference discovery, semantic metadata, optional host metadata, UTF-8, and portable-link checks.
- Added deterministic self-tests and atomic clean-unpack package verification.

## 25.2.0 — 2026-07-29

- Rechecked `oil-oil/beautify-github-readme` against current `main` and pinned commit `55bdb1c05414cd7a0cf911d02e55ece79777206e`; the supplied archive already contained the latest hybrid composition additions.
- Updated Humanizer from the supplied v2.8.2 snapshot to upstream v2.9.1 at `523374dee72d67c7b2b5f858ea0094ffda49c3ac`.
- Added no-fabrication, information-over-shape, voice-sample precedence, pasted/file/embedded invocation modes, and portable metadata behavior to every modular and standalone edition.
- Added explicit `HUMANIZE` routing and specialist execution without forcing a theatrical panel.
- Replaced substring routing with token-aware regex rules and added false-positive regression tests.
- Removed hardcoded portable version strings; `render_portable.py` now derives the version and regenerates LITE plus all standalone editions.
- Added reproducibility checks for portable files, repository-wide local-link validation, upstream source/license validation, and safer frontmatter fallback parsing.
- Added `UPSTREAM_SOURCES.json`, `references/upstream_integration.md`, `scripts/check_upstream.py`, and `UPSTREAM_MAINTENANCE_STANDALONE.md`.
- Made ZIP timestamps reproducible, preserved executable bits for scripts, rejected output-inside-root packaging, and verified path/CRC/root-folder safety after creation.
- Flattened runtime references to one level for stricter host compatibility and added open-spec checks for frontmatter fields, name/description limits, and resource layout.
- Expanded the README auditor with alt-text, project-boundary, active-SVG, external-raster, and CSS-resource checks; packaging now runs validation and evals by default.

## 25.1.0 — 2026-07-29

- Integrated the supplied MIT-licensed `beautify-github-readme` skill as the `README_STUDIO` specialist route.
- Added whole-README, asset-only, and audit-only scope gates with read-only-first authorization boundaries.
- Added project-story extraction, content architecture, project-native hero, visual direction, SVG, hybrid PNG/WebP, and opt-in GitHub-safe GIF methods.
- Added README Information Architect, Maintainer/Developer Advocate, Visual Systems Designer, and Accessibility/SVG Reviewer functions.
- Added `GITHUB_README_STUDIO_STANDALONE.md` and compiled the complete README methodology into both universal monoliths.
- Bundled the README/SVG audit script and optional motion renderer, plus README routing evals and handoff contracts.
- Preserved the upstream MIT license and omitted non-runtime showcase media to keep the skill portable.

## 25.0.0 — 2026-07-29

- Rebuilt the v24 base around the open Agent Skills structure.
- Fixed version drift across archive, YAML, universal files, scripts, evals, and templates.
- Added blind first-pass claim cards, sparse P2P review, evidence arbitration, persuasion resistance, and debate/ensemble gating.
- Replaced hardcoded provider tables with capability-based routing and dated-environment guidance.
- Added scope cards, state capsules, context compression, work splitting, sandbox mode, tool budgets, optimization loop, and holdout evals.
- Integrated prompt-engineering contracts and preserved the complete Humanizer pattern catalog with factual-integrity rules.
- Preserved the supplied `prompt.md` verbatim as a security-audit reference and standalone portable file.
- Added deterministic rendering, validation, evaluation, and ZIP packaging scripts.
- Added complete Markdown/TXT monoliths and a low-context LITE edition for AIs without skills support.
