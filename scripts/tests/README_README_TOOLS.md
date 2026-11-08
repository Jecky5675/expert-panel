# README maintenance tools

These scripts are optional. They are useful when maintaining Expert Panel or when README Studio creates local SVG or GIF assets.

## Check a README and its local SVG files

```bash
python scripts/audit_readme.py README.md --root .
python scripts/audit_readme.py README.md --root . --strict
python scripts/audit_readme.py README.md --json
```

The auditor uses the Python standard library. It checks that local image paths resolve, alt text is present, SVG files are valid XML, and potentially active or unsupported SVG/URI features are reported. It also checks for path escapes, duplicate SVG IDs, external raster dependencies, and oversized input.

Normal errors return a failing exit code. `--strict` also treats warnings as failures. JSON output is available for CI or editor integrations.

The tool is a structural and accessibility check, not a replacement for opening the README on GitHub and looking at it at desktop and mobile widths.

## Render an approved motion GIF

```bash
python scripts/render_readme_motion_gif.py --help
```

Motion is optional. The renderer validates its JSON specification and source SVG before calling local rendering programs. It limits dimensions, duration, frame count, palette size, and output size, and it prevents the output from overwriting the inputs.

The renderer needs Pillow, `ffmpeg`, and either `rsvg-convert` or macOS `sips`. Keep the static SVG as the editable fallback.
