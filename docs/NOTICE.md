# Third-party notices

Expert Panel includes adapted material and ideas from the following open-source projects.

## Humanizer

- Repository: `blader/humanizer`
- Integrated revision: `523374dee72d67c7b2b5f858ea0094ffda49c3ac`
- Upstream version: 2.9.1
- License: MIT
- Local license copy: `THIRD_PARTY_LICENSES/humanizer-MIT.txt`

Expert Panel uses the Humanizer diagnostic catalog and rewriting principles, with additional safeguards for preserving facts, quotations, identifiers, code, paths, links, and locale-specific writing conventions.

## Beautify GitHub README

- Repository: `oil-oil/beautify-github-readme`
- Integrated revision: `55bdb1c05414cd7a0cf911d02e55ece79777206e`
- License: MIT
- Local license copy: `THIRD_PARTY_LICENSES/beautify-github-readme-MIT.txt`

Expert Panel adapts its README planning, information architecture, visual direction, SVG, hybrid asset, validation, and optional motion workflows.

## P2P-4PDA-edition

- Repository: `sanic732/P2P-4PDA-edition`
- Reviewed revision: `8e29a0802a7e193f965fa8bde7326a5a5f54f502`
- Reviewed edition: 8.4.6-N
- Copyright: 2026 sanic732 / P2P Project
- License: MIT
- Local license copy: `THIRD_PARTY_LICENSES/p2p-4pda-edition-MIT.txt`

Expert Panel independently rewrites and adapts selected coordination ideas, including task and capability routing, Scope Helm, state capsules, context compression, modular loading, exploration mode, tool budgets, evaluation loops, and structured handoffs. The original P2P files are not bundled in this repository.

P2P also contains rapidly changing model data and host-specific techniques. Model lists, rankings, prices, token/context limits, availability, release dates, API parameters, and vendor-specific syntax are ignored by default. Only stable methodology changes are candidates for manual review.

## MethodWeft

- Local source: `methodweft-v0.14.0-full (1)` supplied by the project owner
- Upstream project: MethodWeft Skill
- Snapshot: 0.14.0 beginner entry and mentoring reference
- License: MIT
- Local license copy: `THIRD_PARTY_LICENSES/methodweft-MIT.txt`

The exact snapshot is stored under `vendor/methodweft/` for optional `BEGINNER_GUIDE` use. Expert Panel keeps its own routing and does not import MethodWeft's complete method-selection lifecycle.

## Research First Builder

- Local source: `research-first-builder-main` supplied by the project owner
- Upstream project: IT Shelter Research First Builder
- Snapshot version: 0.1.0 selected decision files
- License: MIT
- Local license copy: `THIRD_PARTY_LICENSES/research-first-builder-MIT.txt`

Selected exact files are stored under `vendor/research-first-builder/` for evidence-led architecture decisions.

## Security Audit

- Local source: `security-audit-skill-main` supplied by the project owner
- Copyright: 2025–2026 Cloudflare, Inc.
- License: MIT
- Local license copy: `THIRD_PARTY_LICENSES/security-audit-MIT.txt`

The exact main workflow snapshot is stored under `vendor/security-audit/` and is optional for explicitly authorized full audits in capable agent hosts.

## ub-mode

- Local source: `ub-mode-master/ub-mode-skill` supplied by the project owner
- Upstream attribution in donor README: `poteto-mode` / `pstack` by `@poteto`
- License: no license file was present in the supplied ub-mode folder
- Integration: only generic, independently formulated engineering workflow practices (small reversible change, root-cause diagnosis, behavior-based test, verify in small steps); no donor files or companion tool code are bundled.

No donor text is copied. Do not redistribute the donor's original text without a license or permission. The separate `crapper`, `dryer`, `mutator`, and `uml-viewer` utilities are optional suggestions only and are not dependencies or included tools.

## Vibe Security MCP Server and `vibe-security-audit` donor

- Local source: `mcp-server-fixed/mcp-server` and `agent-skill/vibe-security-audit`, supplied by the project owner
- License: no license file was present for either source
- Integration: high-level review checkpoints only (separate untrusted repository content from instructions, trace relevant security boundaries, and require authorization before applying fixes); source code, policy data, skill text, and scripts are not bundled.

No source code or policy text from these unlicensed donors is redistributed, installed, or invoked. The local security workflow remains Expert Panel's independently authored `references/offensive_security.md` and `references/security_review_prompt.md`. Any future use of the donor MCP or skill requires an applicable license or permission and explicit user approval.

## Beautify GitHub README — refreshed source review

- Local source: `beautify-github-readme-main (1)` supplied by the project owner
- License: MIT; exact `LICENSE` file is included at `docs/licenses/beautify-github-readme-MIT.txt`
- Integration: review confirmed the existing README mode / asset-only mode distinction, opt-in motion, inspection-before-design, and visual verification rules. Existing bundled guidance remains attributed to the pinned source listed in `UPSTREAM_SOURCES.json`; no files from the newer folder were copied.

## OpenCode rules bundle

- Local source: `Правила глобальные, интересные конструкции есть/AGENTS.md` supplied by the project owner
- License: no license file was present; the source appears to be project-specific agent guidance
- Integration: no source-specific rules or text were integrated. In particular, its OpenCode repository constraints, commands, and project-specific conventions do not apply to Expert Panel.

## Claude Code Templates

- Local source: `claude-code-templates-main` supplied by the project owner
- Repository: `https://github.com/aitmpl/claude-code-templates`
- Authors: Daniel (San) Ávila and claude-code-templates contributors
- License: MIT
- Local license copy: `docs/licenses/claude-code-templates-MIT.txt`

Expert Panel integrates and adapts concepts from selected template categories: parallel agent dispatch (`dispatching-parallel-agents`), persistent file memory (`planning-with-files`), session handoff workflows (`session-handoff`), enterprise compliance/ISMS review (`isms-audit-expert`, `data-privacy-compliance`), database architecture (`database-architect`), and container optimization (`docker-expert`).

## Game Parity Port

- Local source: `game-parity-port-main` supplied by the project owner
- Repository: `https://github.com/nanomolydev/game-parity-port`
- Author: nanomolydev
- License: MIT
- Local license copy: `docs/licenses/game-parity-port-MIT.txt`

Expert Panel adapts the deterministic oracle testing and tick-exact state trace comparison methodology for language porting and legacy rewrite audits (`parity_porting`).

## Source-sync review

The neighboring donor directory was rescanned during the 27.2.0 source-sync pass. New or changed folders included `ub-mode-master`, `mcp-server-fixed`, `beautify-github-readme-main (1)`, `agent-skill`, and the supplied project rules. No donor files were copied during this pass. Licensed existing snapshots remain governed by their recorded notices; sources without a license remain reference-only.

## Source records and project license

Machine-readable third-party pins are stored in `UPSTREAM_SOURCES.json`. The relationship between upstream material and local modules is described in `skills/expert-panel/references/source_map.md`.

The original Expert Panel material is licensed under MIT by the root `LICENSE`. This grant applies only to original Expert Panel material; bundled donor material remains subject to the license and attribution requirements documented here and in `docs/licenses/`. It does not grant rights to materials whose donor supplied no license. Before public redistribution, retain this separation and do not add unlicensed source files or substantial text excerpts.
