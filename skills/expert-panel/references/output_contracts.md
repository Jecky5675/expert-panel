# Output Contracts

## Compact decision report

```markdown
# Verdict
[Direct answer]

## Confidence and scope
- Depth/overlays:
- Key assumptions:
- Overall confidence:

## Findings
| Priority | Finding | Confidence | Evidence | Implication |

## Disagreements
| Question | Positions | What resolves it |

## Risks / pre-mortem
- Failure scenario:
- Early indicator:
- Mitigation:

## Action plan
| Sequence | Action | Owner/role | Dependency | Success signal |

## Open decisions
- ...
```

## Audit report

```markdown
# Executive result
Counts by severity and the recommended starting point.

## Scope and method
Files/systems reviewed, exclusions, tools, date, limitations.

## Findings
- **[Severity] Title** — `artifact:location`
  - Evidence:
  - Impact:
  - Remediation:
  - Verification:

## Evidence ledger
| ID | Claim/finding | Evidence | Confidence |

## Residual risk
What remains after remediation or outside scope.
```

## Forecast

```markdown
# Base-rate view
# Drivers and uncertainties
# Scenarios: downside / base / upside
# Probability ranges and assumptions
# Leading indicators
# Decisions robust across scenarios
# Update triggers and date
```

## Mediation

```markdown
# Shared facts
# Interests by stakeholder
# Disputed assumptions
# Feasible trade space
# Options and consequences
# Proposed agreement
# Unresolved items and escalation rule
```

## Evidence ledger CSV schema

See `assets/evidence_ledger_template.csv`.

## GitHub README Studio handoff

```markdown
# Scope and mode
- Mode: README / asset-only / audit-only
- Authorized changes:
- Preserved/excluded areas:

# Project story
- Audience:
- One-sentence value:
- Primary proof:
- First successful action:
- Visual theme:

# Deliverables
| Path | Format | Purpose | Editable source | Validation |

# README changes
- Reading-order changes:
- Claims retained/removed and evidence:
- Embed snippets:

# Validation
- GitHub-width and narrow-width preview
- Local image references
- SVG XML, viewBox, title/description, alt text
- Motion/file-size checks when applicable

# Limitations and approval-required actions
- ...
```
