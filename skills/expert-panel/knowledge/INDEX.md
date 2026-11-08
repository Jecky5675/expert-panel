# Expert Panel Knowledge Base

This directory is a **link catalog**, not a traditional database engine and not a cache of page content. It stores structured pointers to durable knowledge sources that panel experts and specialist routes should consult when relevant.

## Files

| File | Role |
| --- | --- |
| `catalog.json` | Machine-readable entries: id, domain, title, url, tags, notes, freshness. |
| `INDEX.md` | Human-readable usage rules for maintainers and models. |

## How experts use it

1. Before first-pass claim cards, match the task domain and tags to catalog entries.
2. Prefer official/primary targets (standards bodies, regulators, project docs) over secondary blogs.
3. Record used entry IDs (`KB-…`) in the evidence ledger as *starting points*, then verify live content when tools allow.
4. Do not invent URLs. If nothing matches, say so and search or mark `UNKNOWN`.
5. Catalog membership is not proof. A listed link can be outdated, incomplete, or off-scope for the current claim.
6. When web access is unavailable, still use titles and notes to orient research and label freshness limits.

## Domains covered

`security`, `architecture`, `operations`, `research`, `prompt_engineering`, `readme`, `accessibility`, `svg`, `legal`, `data`, `ml_evaluation`, `product`, `cost`, `privacy`, `engineering`, `forecasting`.

## Maintenance

- Add entries only with stable public URLs and a clear domain fit.
- Keep notes short and methodology-focused; avoid transient prices, model rankings, or vendor marketing claims.
- Update `updated` in `catalog.json` when the catalog changes.
- Portable editions embed a compact summary of usage rules; full JSON remains in the skill package.
