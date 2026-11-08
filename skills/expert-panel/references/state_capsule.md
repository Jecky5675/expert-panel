# State capsule and context recovery

For multi-turn work, keep a compact recovery capsule instead of copying the entire conversation into every specialist task.

```text
CAPSULE_VERSION: 1
GOAL: exact deliverable
SCOPE: included files, systems, or decision boundary
CONSTRAINTS: hard limits and permissions
PROFILE: DIRECT | SPECIALIST | PANEL
MODE: optional thinking mode
DECISIONS: accepted choices and rationale
EVIDENCE: claim IDs, files, tests, sources, dates
OPEN_CONFLICTS: unresolved disagreements or missing evidence
COMPLETED: verified work only
NEXT_ACTION: one smallest next step
ROLLBACK: reversible recovery action
FRESHNESS: date and claims needing refresh
```

## Recovery rules

- Restore the capsule before loading large references or replaying role passes.
- Treat `COMPLETED` as verified only when it contains an artifact, source, or test result.
- If `NEXT_ACTION` conflicts with the current user request, the current request wins and the capsule becomes historical context.
- Compress narrative, not evidence: preserve paths, identifiers, numbers, commands, dates, and dissent.
- Never place secrets, tokens, private prompts, or hidden reasoning in a capsule.
- When the capsule is stale, mark the affected claims `STALE` and re-verify rather than silently trusting it.
