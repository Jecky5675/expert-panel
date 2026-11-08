# Optional protocol for conflicts with legacy behavior

Use only when a proposed change conflicts with existing behavior, tests, documentation, compatibility requirements, or another actively used path. This is not a mandatory preflight for all work. Its purpose is to preserve user data and make a deliberate compatibility decision, not to freeze a codebase or require a large panel.

## 1. Establish the actual contract

Identify the requested outcome and affected callers/users. Inspect the smallest relevant set of code, tests, configuration, migration history, and documented contract. Check the working tree/diff where available so user changes are not mistaken for baseline. Distinguish observed behavior from intended behavior: an old test might capture a bug; a README might be stale. Record platform/version scope and whether persistent data, serialized format, public API, or user workflow is affected. If evidence is missing, say so rather than claiming historical intent.

## 2. Classify the conflict

- **Correctness or security:** old behavior fails a stated invariant or causes harm; fix with a regression test and note any compatibility cost.
- **Contract or compatibility:** consumers may depend on existing API, file format, database schema, or UI behavior; preserve or migrate intentionally.
- **Documentation drift:** observed implementation and written guidance differ; verify which behavior is required before changing either.
- **Preference / product trade-off:** both behaviors are valid and user's priorities decide; show options with cost and reversibility.
- **Environment / version mismatch:** a result only holds on a specific runtime or dependency; check actual version before generalizing.

## 3. Decide with proportionate evidence

Produce a compact conflict card: **current observable contract → proposed change → who breaks → evidence → alternatives → safest reversible step → verification**. Compare at least preserve, adapt/compatibility shim, and deliberate breaking change when each is plausible. Prefer the smallest fix that meets the user goal; ask the user only for a consequential value choice or action permission. Security and privacy boundaries are not negotiated away by a persona vote. If public API or persistent data changes, specify migration, rollback/backup, and version communication; do not run destructive migration without approval.

## 4. Verify and report

Use a narrow reproducible test covering both the requested behavior and an important old caller or edge case. If unavailable, give a concrete manual check and label it unrun. Document exactly what remains compatible, what changes, and unresolved assumptions. Stop when evidence supports a decision or an explicit user choice is necessary. Do not claim that several role labels provide independent corroboration of the same source.
