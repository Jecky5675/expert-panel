# Example — README_STUDIO route

Request: “Audit this repository README and redesign only the hero and workflow diagram. Do not rewrite the body.”

Routing:

- Trigger: yes
- Depth: QUICK specialist route
- Overlay: README_STUDIO + AUDIT
- Hard scope: audit entire README; edit only hero and workflow assets
- Roles when useful: Maintainer/Developer Advocate, Visual Systems Designer, Accessibility/SVG Reviewer

Deliverables:

1. Audit findings with evidence from repository files.
2. Project brief and frozen visual system.
3. Editable SVG sources and rendered previews.
4. Optional embed snippets, not inserted without approval.
5. Validation report from `scripts/audit_readme.py` plus visual checks.
