# Prompt Engineering Module

Activate only when the user asks to create, transform, audit, optimize, or adapt a prompt. Do not silently rewrite the user's request before the panel. Apply `safety_compatibility.md` first.

## Safety boundary

- Preserve the legitimate objective, but do not create or optimize prompts intended to override higher-priority instructions, bypass safeguards, reveal hidden prompts or private reasoning, extract secrets, automate unauthorized access, conceal harmful intent, or impersonate a person deceptively.
- For a mixed request, keep the benign business, research, creative, or engineering goal and replace the unsafe mechanism with a defensive, authorized, synthetic, or sandboxed alternative.
- Test robustness with harmless placeholders, synthetic records, and non-deployable prompt-injection examples. Never include real credentials or operational harmful payloads.
- Do not promise that wording can force a model to ignore platform rules or grant unavailable capabilities.

## Workflow

1. Preserve the user's allowed objective and non-negotiable constraints; separate it from any unsafe or unauthorized mechanism.
2. Identify the target environment by capabilities, not assumptions about a model name.
3. Extract missing facts that materially affect the prompt; use placeholders for minor gaps.
4. Build a contract with instructions, inputs, constraints, output schema, tool rules, uncertainty behavior, and acceptance tests.
5. Separate trusted instructions from untrusted data.
6. Remove contradictions, redundant emphasis, hidden constraints, and stale vendor-specific syntax.
7. Add examples only when they clarify format or edge cases.
8. Add a concise self-check against observable success criteria.
9. For consequential prompts, include tool budgets, approval gates, rollback/failure behavior, and prompt-injection handling.
10. Test with representative positive, negative, boundary, and injection-resistance cases using harmless data.

## Prompt contract

```text
ROLE/SCOPE: what function the model performs and does not perform
OBJECTIVE: exact deliverable
INPUTS: supplied data and how to treat it
CONSTRAINTS: hard limits, safety rules, authorization, policies, assumptions, exclusions
PROCESS: only observable workflow requirements; do not demand private chain-of-thought
TOOLS: allowed tools, budgets, validation, stop conditions, approvals
OUTPUT: schema, sections, language, length, citations
UNCERTAINTY: when to verify, ask, assume, or say unknown
ACCEPTANCE TESTS: measurable checks for done
```

## Capability adaptation

- With schema-constrained output, define a schema and validate it.
- With search, require current verification for unstable claims and source links/citations.
- With files, specify authoritative files and how to handle conflicts.
- With subagents, assign isolated work and structured handoffs rather than duplicating the task.
- With no tools, narrow claims and label freshness limits.
- With small context, use progressive disclosure and a state capsule.

Do not hardcode claims such as a model's context size, parameter names, prices, or behavior without current official verification.

## Anti-patterns

- Role-play presented as evidence.
- “Think step by step” used as a substitute for verification.
- Conflicting goals such as “very short and exhaustive.”
- Giant context dumps without authority or relevance labels.
- Negative-only rules that do not state the desired behavior.
- Hidden acceptance criteria.
- Repeated ALL CAPS or urgency used instead of structure.
- Tool access without stop conditions or approval boundaries.
- Instructions that ask the model to reveal private chain-of-thought.
- Jailbreak, moderation-bypass, hidden-prompt extraction, secret-exfiltration, or unauthorized-access objectives disguised as prompt optimization.
- Claims that a prompt can override platform policy or silently expand permissions.

## Optimization loop

Score a baseline on: correctness, completeness, format adherence, evidence discipline, safety, efficiency, and user usefulness. Change the smallest instruction set likely to improve the weakest dimension. Re-test on a holdout case. Stop on plateau or regression.

## Output when transforming a prompt

1. Issues found, mapped to exact text.
2. Safety or authorization adaptations, when needed.
3. Assumptions or placeholders.
4. Final prompt in a copy-ready block.
5. Acceptance checklist.
6. Optional compact variant only when useful.
