# Security and release verification

Expert Panel is primarily a collection of Markdown workflows. It also includes Python tools for validation, packaging, upstream checks, and optional README rendering. Those tools run only when a user, maintainer, AI host, or CI workflow explicitly starts them.

## What was checked for v25.9.2

The public release was reviewed and rebuilt from a clean directory. The release gate included:

- review and compilation of every Python script;
- 54 routing evaluations and 13 deterministic self-test groups;
- regeneration and byte comparison of all portable editions;
- validation of Markdown links, local images, and SVG files;
- scanning the public tree for common credential formats, private keys, local machine paths, and unexpected files;
- deterministic ZIP creation, CRC checking, safe-path checking, and a second full validation after clean extraction;
- safety-boundary regression checks across the core, Prompt Engineer, Security Review, Humanizer, and portable editions;
- two independent builds with matching SHA-256 hashes.

The final release did not contain API keys, private keys, `.env` files, local agent configuration, user data, build notes, or hidden conversation files.

## Network and command behavior

Normal use of the Markdown skill does not contact the internet by itself.

- `scripts/check_upstream.py` makes read-only requests to the public GitHub API when it is run. It compares commit hashes and does not download, install, or modify upstream code.
- `scripts/render_readme_motion_gif.py` can call locally installed rendering programs when the maintainer explicitly runs it.
- Packaging and validation scripts work on the selected project directory and temporary build directories.
- The repository contains no telemetry or background update service.

The AI platform may still provide web access, file access, code execution, or connectors. Those capabilities are controlled by the platform and the permissions granted by the user, not by this repository alone.

## What the checks mean

Passing the release gate shows that the package matches its documented structure and that the included regression cases pass. It is not a promise that every AI response will be correct or that an undiscovered defect is impossible.

Before using any downloaded skill with sensitive files, review its contents and the permissions available to the AI host. For public releases, run:

```bash
python scripts/audit_release.py .
python scripts/package_skill.py . --output ../expert-panel-release.zip
```

## Reporting a problem

For an ordinary bug, open a GitHub issue with the affected version, environment, steps to reproduce, and relevant output.

For a vulnerability that would expose private data, execute unintended commands, or make a validated release contain unsafe files, use GitHub private vulnerability reporting when it is enabled. A concise reproduction is enough; please avoid posting sensitive data or a working exploit in a public issue.

Security fixes target the latest release and should include a regression test when practical.
