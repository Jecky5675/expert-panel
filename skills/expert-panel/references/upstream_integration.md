# Upstream integration and updates

## Tracked projects

| Local area | Repository | Pinned revision | Default update policy |
| --- | --- | --- | --- |
| Humanizer | `blader/humanizer` | `523374dee72d67c7b2b5f858ea0094ffda49c3ac` / v2.9.1 | Treat a newer commit as actionable; inspect relevant behavior and fixes. |
| README Studio | `oil-oil/beautify-github-readme` | `55bdb1c05414cd7a0cf911d02e55ece79777206e` | Treat a newer commit as actionable; inspect methods, tools, and compatibility changes. |
| Coordination methodology | `sanic732/P2P-4PDA-edition` | `8e29a0802a7e193f965fa8bde7326a5a5f54f502` / 8.4.6-N | Advisory only. Report that the repository changed, but do not fail the default check or assume integration is needed. |

The machine-readable pins, policies, and license paths are stored in `UPSTREAM_SOURCES.json`.

## What `check_upstream.py` does

The script asks the public GitHub API for the current commit on each configured branch and compares it with the pinned commit. It does not clone repositories, install code, edit Expert Panel, or publish anything.

Possible statuses:

- `current` — branch tip equals the pinned commit;
- `update-available` — an actionable specialist source changed; default exit code is `1`;
- `advisory-update` — P2P or another advisory methodology source changed; default exit code remains `0`;
- `unavailable` — the GitHub request could not be completed.

Use `--fail-on-advisory` only when you intentionally want every P2P commit to make CI fail:

```bash
python scripts/check_upstream.py . --fail-on-advisory
```

## P2P default-ignore policy

P2P is not a direct runtime dependency. Expert Panel uses selected stable coordination ideas from it, so most P2P releases do not require an Expert Panel update.

Ignore these categories by default:

- model catalogs, rankings, and recommended model assignments;
- prices, billing details, and provider promotions;
- token limits and context-window sizes;
- model availability, release dates, retirement dates, and provider status;
- vendor-specific syntax, API parameters, UI behavior, and host workarounds;
- P2P edition packaging, menus, and release mechanics that do not change reusable methodology.

Review only changes that may improve stable, vendor-neutral behavior, such as:

- scope and success-criteria management;
- capability-based routing;
- context compression and state handoff;
- tool budgets and failure handling;
- evaluation, regression, and evidence methods.

Even in those areas, integration is manual. A new commit is not evidence that Expert Panel should change.

## Update procedure

1. Run `python scripts/check_upstream.py .` with network access.
2. For `update-available`, inspect the relevant commits and files.
3. For `advisory-update`, do nothing unless the release notes or diff suggest a stable methodology improvement.
4. Exclude the P2P default-ignore categories listed above.
5. Integrate only behavior that improves Expert Panel and fits its universal design.
6. Update attribution and license records when necessary.
7. Regenerate portable editions and add regression tests.
8. Run the full validation and packaging gate.
9. Move the pinned commit only after a documented review; do not advance it merely to silence an advisory.
