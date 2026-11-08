#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from pathlib import Path

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_REFERENCES = {
    "host_profiles.md", "role_registry.md", "role_orchestration.md",
    "skill_orchestration.md", "specialist_registry.json", "donor_practice_cards.md",
    "practices_catalog.md", "offensive_security.md", "security_review_prompt.md",
    "mentor_path.md", "evidence_and_research.md", "packs/manifest.json"
}

def parse_scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value

def fallback_yaml_mapping(raw: str) -> dict[str, object]:
    data: dict[str, object] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if "\t" in line or line.startswith(" "):
            raise ValueError(f"unsupported indentation at line {i + 1}")
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line {i + 1}")
        key, value = line.split(":", 1)
        key = key.strip()
        if key in data:
            raise ValueError(f"duplicate key: {key}")
        value = value.strip()
        if value in {"|", ">"}:
            block = []
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                block.append(lines[i][2:] if lines[i].startswith("  ") else "")
                i += 1
            data[key] = ("\n" if value == "|" else " ").join(block).strip()
            continue
        if value == "":
            nested: dict[str, object] = {}
            i += 1
            while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                nested_line = lines[i]
                if not nested_line.strip():
                    i += 1
                    continue
                nested_key, nested_value = nested_line.strip().split(":", 1)
                nested[nested_key.strip()] = parse_scalar(nested_value.strip())
                i += 1
            data[key] = nested
            continue
        data[key] = parse_scalar(value)
        i += 1
    return data

def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if text.startswith("\ufeff"):
        raise ValueError("must not start with BOM")
    if not text.startswith("---\n"):
        raise ValueError("must start with ---")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("closing --- missing")
    raw = text[4:end]
    data = fallback_yaml_mapping(raw)
    return data, text[end + 5:]

def validate_openai_metadata(root: Path) -> list[str]:
    path = root / "openai.yaml" if (root / "openai.yaml").is_file() else root / "skills" / "openai.yaml"
    if not path.is_file():
        return ["missing openai.yaml"]
    return []

def locate(path: Path):
    path = path.expanduser().resolve()
    for payload in (path, path / "skills" / "expert-panel", path / "expert-panel"):
        if (payload / "SKILL.md").is_file():
            repo = payload.parents[1] if payload.parent.name == "skills" else payload.parent
            return repo, payload
    raise FileNotFoundError(f"Could not locate skills/expert-panel/SKILL.md under {path}")

def validate(path: Path) -> list[str]:
    repo, payload = locate(path)
    errors = []
    skill_text = (payload / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r'^\s*version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)', skill_text, re.M)
    if not match:
        errors.append("SKILL.md metadata.version missing")
    else:
        version = match.group(1)
        if f"# Expert Panel v{version}" not in skill_text:
            errors.append("SKILL.md title/version mismatch")

    if len(skill_text.splitlines()) > 500:
        errors.append("SKILL.md exceeds 500 lines")

    for name in sorted(REQUIRED_REFERENCES):
        if not (payload / "references" / name).is_file():
            errors.append(f"Missing references/{name}")

    for p in payload.rglob("*.md"):
        text = p.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            raw = target.strip().strip("<>")
            if not raw or raw.startswith(("#", "mailto:")) or "://" in raw:
                continue
            name = raw.split("#", 1)[0].split("?", 1)[0]
            if not name:
                continue
            resolved = (p.parent / name).resolve()
            try:
                resolved.relative_to(payload.resolve())
            except ValueError:
                errors.append(f"Link escapes payload: {p.relative_to(payload)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"Broken payload link: {p.relative_to(payload)} -> {target}")

    try:
        reg = json.loads((payload / "references/specialist_registry.json").read_text(encoding="utf-8"))
        expected = ["EXACT_HOST_SKILL", "BUNDLED_FULL", "BUNDLED_COMPACT", "REMOTE_REFERENCE"]
        if reg.get("resolution_order") != expected:
            errors.append("Skill resolution priority is incorrect")
        if len(reg.get("roles", {})) < 15:
            errors.append("Specialist registry unexpectedly small")
    except Exception as exc:
        errors.append(f"Invalid specialist registry: {exc}")

    host = (payload / "references/host_profiles.md").read_text(encoding="utf-8")
    for token in ("Web chat", "AI agents", "one canonical", "subagent"):
        if token.casefold() not in host.casefold():
            errors.append(f"Host profiles missing {token}")

    offensive = (payload / "references/offensive_security.md").read_text(encoding="utf-8")
    for token in ("attacker", "exploitability", "attack chain", "authorization"):
        if token.casefold() not in offensive.casefold():
            errors.append(f"Offensive security missing {token}")

    required_repo_files = (
        "README.md", "README_RU.md", "docs/INSTALLATION.md", "docs/DONOR_INVENTORY.json",
        "docs/licenses", "scripts/universal_installer.py", "scripts/export_formats.py",
        "scripts/node/package.json", "scripts/python/pyproject.toml", "scripts/tests/ci_expected.json"
    )
    for rel in required_repo_files:
        if not (repo / rel).exists():
            errors.append(f"Missing repository component {rel}")

    top_dirs = {p.name for p in repo.iterdir() if p.is_dir() and p.name not in {".git", "__pycache__"}}
    if top_dirs != {"skills", "docs", "scripts"}:
        errors.append(f"Repository must contain exactly skills/, docs/, scripts/ at top level; found: {sorted(top_dirs)}")

    try:
        inventory = json.loads((repo / "docs/DONOR_INVENTORY.json").read_text(encoding="utf-8"))
        if len(inventory.get("bundles", [])) < 30:
            errors.append("Donor inventory is incomplete")
    except Exception as exc:
        errors.append(f"Donor inventory invalid: {exc}")

    for p in repo.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".zip", ".whl", ".tgz"}:
            errors.append(f"Generated archive in source tree: {p.relative_to(repo)}")

    return sorted(set(errors))

def main():
    parser = argparse.ArgumentParser(description="Validate Expert Panel source layout and payload")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    try:
        errors = validate(Path(args.root))
    except Exception as exc:
        errors = [str(exc)]
    for error in errors:
        print("ERROR:", error)
    print(f"Validation: {len(errors)} error(s)")
    raise SystemExit(1 if errors else 0)

if __name__ == "__main__":
    main()
