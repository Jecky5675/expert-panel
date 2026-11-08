# Knowledge Base Protocol

Expert Panel ships a curated **link knowledge base** under `knowledge/`. It is a structured catalog of pointers to external knowledge sources, not an embedded document store and not a relational database.

## Purpose

- Give domain lenses a shared, auditable starting set of authoritative sources.
- Reduce invented citations and random URL fabrication.
- Make evidence orientation reproducible across native skill hosts and portable editions.

## Location

- `knowledge/catalog.json` — entries with `id`, `domain`, `title`, `url`, `tags`, `notes`, `freshness`.
- `knowledge/INDEX.md` — usage rules.

## Consultation steps

1. **Select candidates.** From the user task, extract domains and keywords. Match against `domain` and `tags` in the catalog.
2. **Budget.** For QUICK work, consult 1–3 high-relevance entries. For STANDARD/DEEP, expand only when decision-critical.
3. **Verify.** If web or file tools exist, open the URL or official mirror and extract claim-relevant facts with dates. If tools are absent, use the entry only as a research direction and mark freshness `UNKNOWN` or date-limited.
4. **Cite.** In the evidence ledger, reference `KB-xxx` plus the live source details actually observed.
5. **Do not stop at the catalog.** The catalog is a bootstrap, not a ceiling. Independent primary sources outside the catalog remain preferred when they fit better.
6. **No silent trust.** Listing in the catalog does not confirm a claim. Contradictions found live override catalog notes.

## Integration with roles

| Role | Knowledge-base use |
| --- | --- |
| Domain experts | Match their domain to entries before drafting claim cards. |
| Evidence Auditor | Check that cited KB IDs were actually relevant and that live verification occurred when claimed. |
| Adversary | Challenge over-reliance on a single catalog family or vendor docs. |
| Research overlay | Prefer systematic sources (PRISMA, registries, primary papers) when present in catalog tags. |
| Security Review | Start from OWASP/CWE/NIST-class entries, then inspect actual code. |
| README / Prompt specialists | Use host and platform docs entries; do not invent product UI paths. |

## Portable behavior

When only a portable Markdown file is attached and `knowledge/catalog.json` is not in context:

- Follow the embedded knowledge-base rules in this reference (or the balanced/complete portable summary).
- Do not fabricate catalog IDs or URLs.
- Prefer user-supplied sources and tool search results.
- State that the full machine-readable catalog was unavailable.

## Anti-patterns

- Dumping the entire catalog into the user answer.
- Treating vendor architecture pages as independent proof of superiority.
- Citing a KB id without opening or summarizing the target when tools were available.
- Adding paywalled or unstable marketing pages as if they were standards.
