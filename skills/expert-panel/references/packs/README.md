# Capability packs

Capability packs are bounded workflow families. They point to canonical references in the parent `references/` directory and must not be treated as proof that every donor skill is installed or active.

- `manifest.json` records pack status and donor families.
- `status=core` is always available.
- `status=integrated_fallback` is a local fallback method.
- `status=experimental` requires explicit task scope and verification.
- `status=reference_only` is informational and does not authorize execution.
