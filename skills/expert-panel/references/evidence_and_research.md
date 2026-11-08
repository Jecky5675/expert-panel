# Evidence and Research Protocol

## Evidence hierarchy

Use the strongest source available for the claim:

1. direct observation, reproducible test, official record, statute/regulation, original dataset, primary research, vendor documentation for its own product;
2. systematic review, standards body, regulator guidance, reputable secondary analysis;
3. expert inference grounded in named evidence;
4. anecdote or community report, clearly labeled;
5. unsupported model recall, which must not be presented as verified.

Source quality is claim-dependent. A vendor is primary for documented API syntax but not an independent source for comparative superiority.

## Research loop

0. Consult `knowledge/catalog.json` for domain-matching `KB-…` starting points (see [knowledge_base.md](knowledge_base.md)); verify live targets when tools allow.
1. Convert the question into atomic claims and decision criteria.
2. Mark which claims are temporally unstable or high-stakes.
3. Search for primary evidence first.
4. Triangulate decision-critical claims with an independent source or direct test.
5. Check event date separately from publication date.
6. Record contradictions instead of selecting the convenient source silently.
7. Stop when additional searches are unlikely to change the decision, not merely when many links have been collected.

## Evidence ledger

| ID | Atomic claim | Source/artifact | Type | Event/pub date | Accessed | Supports/contradicts | Independence | Confidence | Freshness |
|---|---|---|---|---|---|---|---|---|---|

## Claim discipline

- One row per atomic claim.
- Quotes must be short and exact; paraphrases must preserve the source's qualification.
- A source that cites another source does not automatically count as independent.
- Missing evidence is `UNKNOWN`, not a license to fill gaps.
- Numeric estimates include unit, denominator, time period, and uncertainty.
- Forecasts identify drivers, scenarios, leading indicators, and update triggers.

## Hypothesis protocol for DEEP work

For 3–5 hypotheses record:

```text
HYPOTHESIS
PRIOR: low/medium/high, with basis
CONFIRMING OBSERVATION
DISCONFIRMING OBSERVATION
OWNER
FINAL STATUS
KEY EVIDENCE IDS
```

Include at least one plausible contrarian hypothesis. Disconfirmation is a useful result.

## Current-information rule

When a claim may have changed, verify it during the task if a current source tool exists. Use exact dates and versions. If verification is impossible, say what is known from the supplied material and what remains unverified.

## Multi-agent evidence warning

Agreement among several simulated roles is not source triangulation. Multiple agents may share the same model, training data, prompt, or error. Treat their agreement as an aggregation signal only.

## Research stopping rule

Stop when:

- every decision-critical claim is confirmed, supported, conflicted, or explicitly unknown;
- remaining uncertainty is unlikely to change the recommendation, or is surfaced as an open decision;
- source quality and freshness are sufficient for the risk level;
- a new search round yields mostly duplicates.

## Research basis for the protocol

The design deliberately avoids claiming that debate is always superior. Recent evaluations report that simple independent ensembling can match or outperform debate in many settings, while heterogeneous roles and sparse communication can improve efficiency. Research also shows that a persuasive adversarial participant can drive false consensus. Therefore Expert Panel uses blind first passes, content-anonymous review when possible, method diversity, evidence-based correction, sparse topology, an independent ensemble baseline, a debate-value gate, and a separate Evidence Auditor.

Selected reading:

- Choi, Zhu, Li (2025), “Debate or Vote: Which Yields Better Decisions in Multi-Agent Large Language Models?”
- Choi, Zhu, Li (2025), “When Identity Skews Debate: Anonymization for Bias-Reduced Multi-Agent Reasoning.”
- Liang et al. (2023), “Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate.”
- Zhang et al. (2025), “If Multi-Agent Debate is the Answer, What is the Question?”
- Li et al. (2024), “Improving Multi-Agent Debate with Sparse Communication Topology.”
- Kraidia et al. (2026), “When collaboration fails: persuasion driven adversarial influence in multi agent large language model debate.”
- Agent Skills open specification: https://agentskills.io/specification
