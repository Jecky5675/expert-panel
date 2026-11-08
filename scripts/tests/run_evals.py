#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from panel_router import route

MAX_CASES = 10_000
MAX_REPEAT_COUNT = 10_000
MAX_PROMPT_CHARS = 200_000


def materialize_prompt(case: dict) -> str:
    if not isinstance(case, dict):
        raise ValueError("eval case must be an object")
    prompt = str(case.get("prompt", ""))
    repeat = case.get("repeat")
    if repeat is not None:
        if not isinstance(repeat, dict):
            raise ValueError("repeat must be an object")
        count = repeat.get("count", 0)
        if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= MAX_REPEAT_COUNT:
            raise ValueError(f"repeat.count must be an integer between 0 and {MAX_REPEAT_COUNT}")
        text = str(repeat.get("text", ""))
        if len(text) * count > MAX_PROMPT_CHARS:
            raise ValueError("repeated eval payload exceeds safety limit")
        prompt += text * count
    if len(prompt) > MAX_PROMPT_CHARS:
        raise ValueError("eval prompt exceeds safety limit")
    return prompt


def compare(got: dict[str, object], expect: dict[str, object]) -> list[str]:
    if not isinstance(expect, dict):
        return ["expect must be an object"]
    issues: list[str] = []
    for key, expected in expect.items():
        if key == "overlays_contains":
            if not isinstance(expected, list) or not set(expected).issubset(set(got.get("overlays", []))):
                issues.append(f"overlays {got.get('overlays')} missing {expected}")
        elif key == "overlays_not_contains":
            if not isinstance(expected, list):
                issues.append("overlays_not_contains must be an array")
                continue
            bad = set(expected).intersection(set(got.get("overlays", [])))
            if bad:
                issues.append(f"overlays unexpectedly contain {sorted(bad)}")
        elif key == "reasons_contains":
            if not isinstance(expected, list):
                issues.append("reasons_contains must be an array")
                continue
            joined = " | ".join(str(item) for item in got.get("reasons", []))
            for fragment in expected:
                if str(fragment) not in joined:
                    issues.append(f"reasons missing {fragment!r}: {joined!r}")
        elif got.get(key) != expected:
            issues.append(f"{key}={got.get(key)!r}, expected {expected!r}")
    return issues


def load_cases(path: Path) -> list[dict]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load evals: {exc}") from exc
    if not isinstance(payload, list) or not 1 <= len(payload) <= MAX_CASES:
        raise ValueError(f"evals must be a non-empty array with at most {MAX_CASES} cases")
    seen: set[str] = set()
    cases: list[dict] = []
    for index, case in enumerate(payload):
        if not isinstance(case, dict):
            raise ValueError(f"eval case {index} must be an object")
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise ValueError(f"eval case {index} has no non-empty id")
        if case_id in seen:
            raise ValueError(f"duplicate eval id: {case_id}")
        seen.add(case_id)
        if "expect" not in case or not isinstance(case["expect"], dict):
            raise ValueError(f"eval case {case_id} has no expect object")
        materialize_prompt(case)
        cases.append(case)
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    candidate = Path(parser.parse_args().root).resolve()
    root = candidate if (candidate / "SKILL.md").is_file() else candidate / "skills" / "expert-panel"
    try:
        cases = load_cases(root / "evals/evals.json")
    except ValueError as exc:
        raise SystemExit(f"invalid eval suite: {exc}") from exc
    failures: list[str] = []
    for case in cases:
        got = route(materialize_prompt(case))
        local = compare(got, case["expect"])
        if local:
            failures.extend(f"{case['id']}: {item}" for item in local)
        print("PASS" if not local else "FAIL", case["id"], got)
    failed_ids = {item.split(":", 1)[0] for item in failures}
    print(f"Evals: {len(cases) - len(failed_ids)}/{len(cases)} cases passed")
    for item in failures:
        print("ERROR:", item)
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
