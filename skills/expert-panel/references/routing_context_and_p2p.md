# Routing, Context, and Sparse P2P Protocol

This module uses portable P2P coordination patterns while avoiding brittle vendor and version tables.

## 1. Capability-based routing

Route by observed capability, not model brand:

| Need | Preferred capability |
|---|---|
| Current facts | live search with source access |
| Repository audit | recursive file search, line-level reads, code execution |
| Deterministic transformation | local script with tests |
| Independent perspectives | isolated subagents or sequential blind passes |
| Specialist composition | installed-skill registry or exact skill invocation |
| Long evidence set | retrieval plus source-linked summaries |
| Strict machine output | schema-constrained generation and validation |
| Consequential action | approval checkpoint and least-privilege tool |

Never embed fast-aging model IDs, prices, context limits, or API parameters in the core skill. Put environment-specific information in a dated local profile and verify it before use.

## 2. Load score

Estimate complexity using 0–2 points each:

- number of distinct domains;
- consequence/reversibility;
- uncertainty or evidence conflict;
- amount of source material;
- adversarial/security exposure;
- need for current verification;
- number of deliverables or dependent stages.

Suggested routing: `0–3 DIRECT/QUICK`, `4–7 STANDARD`, `8+ DEEP or split workstreams`. User-specified depth overrides unless unsafe or impossible.

## 3. Scope Helm

Maintain:

```text
GOAL
SUCCESS CRITERIA
IN SCOPE
OUT OF SCOPE
CONSTRAINTS
ASSUMPTIONS
DEPENDENCIES
CURRENT PHASE
NEXT ACTION
BLOCKERS
```

Detect drift whenever a new section no longer maps to a success criterion. Either remove it or label it as an optional extension.

## 4. Sparse peer graph

Create edges only for:

- direct factual contradiction;
- dependency (one claim requires another);
- risk/reward trade-off;
- competing implementation;
- shared evidence interpreted differently.

Review schedule:

```text
Round 0: blind claim cards
Round 1: anonymized strongest relevant cross-checks plus “what did all cards miss?”
Evidence pass: verify disputed material claims
Round 2: only unresolved decision-changing conflicts
Stop: no new evidence, risk, or test
```

Prefer a hub-and-spoke or sparse graph over all-to-all communication. The Evidence Auditor is a verification hub; the Synthesizer reads final cards, not every verbose message.

## 5. Debate-versus-ensemble gate

Record the independent answer distribution as an ensemble baseline. Before another debate round ask:

- Did the last round identify a factual error?
- Did it add a new source or reproducible test?
- Did it expose a decision-changing assumption or risk?
- Did any expert update for a stated reason?

If all are no, stop. Aggregate the original independent answers using a transparent decision matrix or evidence-weighted ranking. More debate is not automatically better, and majority support does not become evidence.

## 6. Persuasion resistance

- Strip persona/model/provider identity, prestige, and rhetorical flourishes before judging claims.
- Ask the Evidence Auditor to review atomic claims in shuffled order under neutral IDs.
- Separate generation, critique, evidence check, and final synthesis.
- Do not let the same role be adversary and final judge in high-stakes work.
- Require source-linked correction for factual changes.
- Treat unanimous convergence after exposure as a possible warning, not proof.
- Ask what all responses missed; shared omissions are more important than pairwise style disputes.
- Measure reasoning-footprint overlap and label high-overlap agreement `THEATRICAL CONSENSUS`.

## 7. Context compression

Use this order:

1. Delete duplicated instructions and repeated summaries.
2. Keep exact constraints, numbers, identifiers, citations, and open conflicts verbatim.
3. Summarize completed work into claim/evidence/decision records.
4. Move detailed references out of the active context.
5. Preserve a state capsule before major compression or handoff.

Do not summarize a summary repeatedly. Return to source evidence when precision matters.

## 8. State capsule

```yaml
capsule_version: 1
updated: YYYY-MM-DD
question: "..."
success_criteria: []
constraints: []
assumptions: []
decisions: []
evidence_ids: []
open_conflicts: []
risks: []
completed: []
next_action: "..."
artifacts: []
freshness_notes: []
```

A capsule is a transfer format, not hidden memory. Show it when the user asks to move work between systems.

## 9. Sandbox / exploration mode

Use for reversible idea generation or uncertain design:

- mark outputs `EXPERIMENTAL`;
- cap approaches and iterations;
- keep production decisions unchanged;
- define evaluation criteria before selecting a winner;
- formalize only after a quality gate.

## 10. Tool budgets and failure handling

Set a budget appropriate to the task. Stop or reroute when repeated calls return duplicate or low-value results. Log what failed, what fallback was used, and how confidence changed. Never hide unavailable tools behind simulated claims.

## 11. Prompt and response optimization

Use iterative optimization only against explicit criteria:

1. baseline output;
2. score against rubric;
3. identify highest-impact defect;
4. change one or a small coherent set of instructions;
5. rerun representative tests;
6. stop when gains plateau or regressions appear.

Keep a holdout test set to avoid optimizing only for examples already seen.
