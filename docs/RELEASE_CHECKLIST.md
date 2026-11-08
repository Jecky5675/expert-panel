# Release checklist

This checklist is for maintainers preparing a public ZIP or GitHub release. Before public redistribution, the owner must select and document a project-wide license for the original Expert Panel material; bundled MIT notices alone do not grant that permission. Do not publish before this decision and a final rights review.

## 1. Review the change

- Read every changed source, script, evaluation, and public document.
- Confirm that the change works for native Skills and portable editions.
- Check third-party attribution when upstream material changed.
- Review `git status`, `git diff`, and the final tracked-file list.

## 2. Update the version

Keep the version synchronized in:

- `SKILL.md` metadata and heading;
- `README.md`;
- `CHANGELOG.md`;
- `assets/report_template.md`;
- `assets/readme-hero.svg`;
- `.github/workflows/validate.yml`.

Portable files receive the version from the renderer and should not be edited manually.

## 3. Run the local gate

```bash
python scripts/render_portable.py .
python scripts/audit_release.py .
python scripts/validate_skill.py .
python scripts/run_evals.py .
python scripts/role_orchestrator.py --check-cases
python scripts/skill_discovery.py --role architecture --role offensive_security
python scripts/self_test.py .
python scripts/audit_readme.py README.md --root . --strict
python -m compileall -q scripts
```

When network access is available, also run:

```bash
python scripts/check_upstream.py .
```

`--allow-offline` may be used for an offline build, but release notes should then say that the latest upstream commits were not checked by the script.

## 4. Exercise changed guardrails

Add or run a small mutation test for the behavior you changed. Typical examples include a stale portable file, duplicate version, unsafe ZIP path, invalid SVG resource, accidental credential fixture, or a routing false positive.

## 5. Test installer and export

```bash
python scripts/universal_installer.py --target generic --dest ../test-skills --dry-run
python scripts/universal_installer.py --export ../test-export.md
rm -f ../test-export.md
```

## 6. Inspect the source repository

Confirm that the tree contains only the canonical `expert-panel/` directory without duplicate vendor skill copies, unneeded archive ZIPs, or temporary build folders.

## 7. Publish

Publish the repository, changelog entry, and release notes. Describe what was actually tested and avoid claiming capabilities that were not exercised in the build environment.
