# Contributing

Thanks for helping improve Expert Panel. Contributions can be code, documentation, routing examples, tests, portability fixes, or clearer installation guidance.

## Before you start

A useful change should continue to work in both forms of the project:

- the native Agent Skill rooted at `SKILL.md`;
- the portable files used by chats without native Skills.

The short architecture overview is in [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md).

## Where to make changes

Edit the source files first:

- `SKILL.md` for top-level behavior;
- `references/` for detailed methods;
- `scripts/` for deterministic tools;
- `evals/evals.json` for routing cases;
- `assets/` and `docs/` for public material.

Files under `portable/` are generated. After changing the source, rebuild them with:

```bash
python scripts/render_portable.py .
```

## Tests

Choose the smallest test that proves the change:

- add a routing case for activation or false-positive fixes;
- add a deterministic self-test for script behavior;
- add a validator rule for a package invariant;
- update the README/SVG auditor when changing asset handling.

Run the standard checks from the repository root:

```bash
python scripts/render_portable.py .
python scripts/audit_release.py .
python scripts/validate_skill.py .
python scripts/run_evals.py .
python scripts/self_test.py .
python scripts/audit_readme.py README.md --root . --strict
python -m compileall -q scripts
```

To build the same ZIP that CI builds:

```bash
python scripts/package_skill.py . --output ../expert-panel-v25.9.2-github.zip
```

## Documentation style

Write for the person who has just discovered the repository:

- explain the purpose before the architecture;
- define a specialist term the first time it appears;
- give a realistic example instead of only describing rules;
- keep warnings proportional to the actual risk;
- separate instructions for users from details intended for maintainers.

Technical runtime rules may be firm, but public documentation should remain calm, direct, and welcoming.

## Upstream sources

The project tracks Humanizer, Beautify GitHub README, and P2P-4PDA-edition in `UPSTREAM_SOURCES.json`. Review upstream changes before integrating them. P2P is an advisory methodology source. Model lists, prices, context/token limits, release dates, availability claims, and vendor-specific settings are ignored by default.

Keep the third-party license files and attribution entries with any adapted material.

## Pull requests

A helpful pull request explains:

- what changed for users;
- which environments were tested;
- any fallback behavior;
- the tests that cover the change.

Small, focused pull requests are easier to review. It is fine to open an issue first when you are unsure where a change belongs.

## Public repository hygiene

Before committing, check `git status` and run `python scripts/audit_release.py .`. Avoid committing credentials, personal data, local AI configuration, generated ZIP files, caches, or internal work notes.
