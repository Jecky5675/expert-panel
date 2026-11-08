#!/usr/bin/env python3
"""Read-only discovery and fallback resolver for installed specialist skills."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "skills/expert-panel/references/specialist_registry.json"
NAME = re.compile(r"^name:\s*[\"']?([a-z0-9][a-z0-9-]*)", re.M)
DEFAULT_ROOTS = [Path.home()/".agents/skills", Path.home()/".claude/skills", Path.home()/".config/opencode/skills", Path.home()/".gemini/skills", Path.home()/".openclaw/workspace/skills", Path.home()/".hermes/skills"]

def registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))["roles"]

def discover(roots: list[Path]) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for root in roots:
        root = root.expanduser()
        if not root.is_dir() or root.is_symlink(): continue
        for child in [root] + [p for p in root.iterdir() if p.is_dir() and not p.is_symlink()]:
            skill = child / "SKILL.md"
            if not skill.is_file() or skill.stat().st_size > 512*1024: continue
            try: text = skill.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError): continue
            match = NAME.search(text)
            if match: found.setdefault(match.group(1), []).append(str(child.resolve()))
    return found

def resolve(role: str, roots: list[Path]) -> dict:
    data = registry()
    if role not in data: raise ValueError(f"unknown registry role: {role}")
    item, found = data[role], discover(roots)
    candidates = []
    for alias in item["aliases"]:
        for path in found.get(alias, []): candidates.append({"name": alias, "path": path, "status": "DISCOVERED_REVIEW_REQUIRED"})
    return {"role": role, "candidates": candidates, "status": "EXACT_HOST_SKILL_CANDIDATE" if candidates else "BUNDLED_FULL", "fallback_full": item["fallback_full"], "fallback_compact": item["fallback_compact"], "sources": item["sources"], "authorization": item.get("authorization")}

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--role", action="append"); p.add_argument("--roots", action="append", type=Path); p.add_argument("--json", action="store_true")
    a=p.parse_args(); roles=a.role or []
    if not roles: p.error("at least one --role is required")
    result=[resolve(role, a.roots or DEFAULT_ROOTS) for role in dict.fromkeys(roles)]
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
if __name__ == "__main__": raise SystemExit(main())
