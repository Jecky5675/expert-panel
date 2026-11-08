# Architecture

This document is for maintainers and developers. New users can start with the main [`README.md`](../README.md).

## Design goal

Expert Panel keeps one behavior model across four environments:

1. native Agent Skills hosts;
2. local desktop or CLI agents;
3. web interfaces with custom Skill upload;
4. ordinary chats that can only read attached Markdown or text.

The project separates optional automation from the core workflow so that the skill still works when scripts, web access, other skills, or separate agents are unavailable.

## Source files

| Path | Role |
| --- | --- |
| `SKILL.md` | Entry point, routing, shared rules, and output structure. |
| `references/` | Detailed specialist and review methods loaded when needed. |
| `scripts/` | Deterministic validation, routing, audit, packaging, and rendering tools. |
| `evals/evals.json` | Routing regression cases. |
| `evals/role_orchestrator_cases.json` | Deterministic role-planning cases. |
| `evals/behavioral_review_cases.json` | Human-reviewed acceptance prompts, not model-quality test results. |
| `assets/` | Templates and README visuals. |
| `portable/` | Generated self-contained editions for non-skill chats. |
| `knowledge/` | Curated HTTPS link catalog for expert evidence orientation. |

Portable files are built from the modular source with `scripts/render_portable.py`; maintainers should edit the source rather than the generated copies.

## Routing

The router makes three separate choices:

- **execution class:** direct answer, one specialist, or panel;
- **depth:** quick, standard, or deep;
- **task signals:** research, security, planning, forecasting, and other overlays.

Separating these choices keeps long input from being treated as automatically complex and keeps a focused request from creating an unnecessary multi-role process.

`BEGINNER_GUIDE` handles a rough idea without forcing a panel. `PROJECT_REVIEW` scopes an actual repository and selects different evidence-bound lenses. `scripts/panel_router.py` is the canonical deterministic route; `scripts/role_orchestrator.py` consumes that result to produce two role layers (built-in core functions plus dynamic stack/attack/data roles). It prints a planning-only JSON sequence with role cards and stop conditions. It does not inspect files, invoke models, delegate work, or prove findings. The AI host performs the actual review with authorized tools, using `references/role_orchestration.md`, `references/role_registry.md`, `references/mentor_path.md`, `references/host_profiles.md`, and `references/skill_orchestration.md` as needed. The optional older-behavior comparison is in `references/legacy_review_protocol.md`.

## Specialist composition and skill discovery

Specialist capabilities follow a four-tier resolution order defined in `references/specialist_registry.json` and `references/skill_orchestration.md`:

1. `EXACT_HOST_SKILL`: exact skill installed and callable in the host (discovered via `scripts/skill_discovery.py` or host registry).
2. `BUNDLED_FULL`: canonical in-project module under `references/` or `vendor/`.
3. `BUNDLED_COMPACT`: compact fallback for small context windows.
4. `REMOTE_REFERENCE`: official repository reference inspected as data only with user permission.

The universal installer `scripts/universal_installer.py` installs the canonical skill to any supported agent host without duplicate platform directories, or exports a self-contained Markdown file for web chats.

## Panel workflow

A full panel normally contains:

1. a scope summary;
2. several method-diverse first passes;
3. selective review of disagreements and dependencies;
4. evidence checks and deterministic tests where available;
5. alternative options and a reversible experiment;
6. a synthesis that keeps important uncertainty and dissent visible.

When separate agents are unavailable, one model performs sequential review passes and labels them accordingly.

## Release checks

The validator checks metadata, version synchronization, links, portable reproducibility, upstream attribution, required repository files, and script syntax. The release auditor scans the public tree for unexpected files and common accidental-secret patterns. The packager creates a deterministic ZIP, checks its paths and CRC, extracts it into a clean directory, and reruns the full validation suite.

These checks protect the release process; they are not a general proof that every model output is correct. The project-wide license for original Expert Panel content still requires an owner decision before public redistribution (see `NOTICE.md`); donor-role references are not bundled implementations or independently license-cleared assets.
