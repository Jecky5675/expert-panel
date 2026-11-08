# Single-source architecture and installation

Expert Panel maintains **one canonical directory** under `expert-panel/`. It does not create duplicate platform-specific skill folders or require ZIP archives. Platform differences are handled by capability profiles and the universal installer:

- `references/host_profiles.md` — single-model sequential perspectives for web chat; real subagent delegation for capable agent hosts;
- `references/skill_orchestration.md` and `references/specialist_registry.json` — multi-tier capability resolution (exact host skill → bundled full module → bundled compact fallback → remote reference);
- `scripts/universal_installer.py` — fail-closed installation to any supported agent host, or direct export of a single self-contained Markdown file for web chats;
- `scripts/skill_discovery.py` — read-only discovery of installed specialist skills;
- `portable/` — generated self-contained files; do not edit them manually.

## Usage

```bash
# Verify the skill
python scripts/validate_skill.py .
python scripts/run_evals.py .
python scripts/role_orchestrator.py --check-cases
python scripts/self_test.py .

# Install to an agent host
python scripts/universal_installer.py --target generic --dest "~/.agents/skills" --dry-run
python scripts/universal_installer.py --target generic --dest "~/.agents/skills" --yes

# Export for web chat (single Markdown file, no ZIP)
python scripts/universal_installer.py --export "./expert-panel.md"

# Discover installed specialist skills
python scripts/skill_discovery.py --role architecture --role offensive_security
```

This single-source model avoids the drift and duplication issues seen in packages with separate per-vendor skill folders.
