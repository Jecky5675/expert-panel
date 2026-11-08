# Deliberation Quality Controls

## 1. Method diversity, not costume diversity

Assign different cognitive operations before adding more voices. Useful operations include:

- decomposition and first-principles checks;
- inversion and pre-mortem;
- outside-view or base-rate comparison;
- analogy from an adjacent domain;
- dependency graphing and execution sequencing;
- naive-questioning or newcomer review;
- evidence verification and falsification;
- user-impact, safety, or adversarial analysis.

Two roles that use the same evidence path and reasoning operation count as one effective opinion even if their titles differ.

## 2. Expand the option space before judging

For non-trivial choices, do not stop at `A`, `B`, and a compromise `A+B`. Generate:

- `C`: a genuinely different mechanism;
- `D`: a reframed or “neither” option;
- the smallest reversible experiment that would reduce the key uncertainty.

A hybrid is not automatically a synthesis; it may inherit both options' weaknesses.

## 3. Anonymous content review

When the host supports isolated reviewers:

1. Remove author, model, role, provider, and prestige labels from first-pass cards.
2. Randomize card order and assign neutral IDs such as `A`, `B`, and `C`.
3. Ask reviewers to judge atomic claims, evidence, assumptions, and tests, not identity or style.
4. Restore attribution only after reviews are complete when auditability requires it.

If deterministic anonymization is unavailable, at minimum omit role names during critique. Never claim anonymity if reviewers can infer identity from preserved labels or distinctive self-reference.

Every peer-review round must ask: **What did all responses miss?** This catches shared framing errors that pairwise criticism can overlook.

## 4. Ensemble baseline and debate-value gate

Record the independent first-pass distribution before discussion. Treat it as the baseline. Continue debate only if critique produces at least one correction signal:

- a factual error was identified;
- new evidence or a reproducible test appeared;
- a hidden assumption or missing option changed the decision;
- a participant updated for a stated, evidence-linked reason.

If none occurs, stop and synthesize the independent ensemble. Do not describe unchanged repetition as deeper reasoning. Majority support is an aggregation signal, not evidence.

## 5. Consensus diagnostics

Before accepting convergence, check:

- reasoning-footprint overlap: did supposedly diverse roles use the same claims and evidence?
- confidence-evidence alignment: is high confidence backed by stronger evidence?
- persuasion risk: did a fluent but weakly sourced card cause updates?
- minority quality: does a smaller position have the decisive test or strongest source?
- value versus fact: is disagreement about evidence, interpretation, priorities, or values?

Label high-overlap agreement as `THEATRICAL CONSENSUS` and treat it as one effective opinion until independent evidence supports it.

## 6. Judge reliability

For close, high-impact decisions, prefer multiple independent judges or a deterministic decision matrix when capabilities allow. Judges first score separate attributes against precommitted criteria, then make a holistic recommendation. A final reconciliation may merge judge outputs, but must retain unresolved dissent and flip conditions.

Do not create a “jury” from sequential rewrites in one shared context and call it independent. In generic-host fallback, use one transparent synthesizer and state the limitation.

## 7. Research basis and limits

The protocol reflects evidence that blind initial answers can reduce anchoring, anonymous review can reduce identity-driven deference, and method diversity can improve coverage. It also reflects contrary findings: debate can add cost without outperforming simple independent voting, and confident persuasion can amplify error. Therefore Expert Panel uses selective critique, explicit evidence checks, stopping rules, and honest degraded modes rather than assuming that more agents or rounds are better.

Selected sources and comparable open skills are documented in `references/source_map.md`. These sources inspire testable controls; they do not prove that every task benefits from a panel.
