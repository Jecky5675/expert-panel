#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MAX_RESPONSE_BYTES = 1_000_000
REPO_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
BRANCH_RE = re.compile(r"^[A-Za-z0-9._/-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ACTIONABLE_MODES = {"specialist-integration"}
ADVISORY_MODES = {"methodology-advisory"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        return None


def request_json(url: str, timeout: float) -> dict[str, object]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "expert-panel-upstream-check"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(request, timeout=timeout) as response:
        if response.status != 200:
            raise ValueError(f"unexpected HTTP status {response.status}")
        final_url = urllib.parse.urlsplit(response.geturl())
        if final_url.scheme != "https" or final_url.hostname != "api.github.com":
            raise ValueError(f"unexpected response origin: {response.geturl()}")
        content_type = response.headers.get_content_type()
        if content_type not in {"application/json", "application/vnd.github+json"}:
            raise ValueError(f"unexpected content type: {content_type}")
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ValueError("GitHub response exceeds safety limit")
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("GitHub response must be a JSON object")
    return payload


def valid_source(source: object) -> tuple[str, str, str, str, str]:
    if not isinstance(source, dict):
        raise ValueError("source entry must be an object")
    source_id = str(source.get("id", ""))
    repo = str(source.get("repository", ""))
    branch = str(source.get("branch", "main"))
    pinned = str(source.get("integrated_commit", ""))
    mode = str(source.get("tracking_mode", "specialist-integration"))
    if not source_id:
        raise ValueError("source id is missing")
    if not REPO_RE.fullmatch(repo):
        raise ValueError(f"invalid repository: {repo!r}")
    if not BRANCH_RE.fullmatch(branch) or branch.startswith("/") or ".." in branch.split("/"):
        raise ValueError(f"invalid branch: {branch!r}")
    if not SHA_RE.fullmatch(pinned):
        raise ValueError(f"invalid pinned commit for {source_id}: {pinned!r}")
    if mode not in ACTIONABLE_MODES | ADVISORY_MODES:
        raise ValueError(f"unsupported tracking_mode for {source_id}: {mode!r}")
    return source_id, repo, branch, pinned, mode


def commit_url(repo: str, branch: str) -> str:
    owner, name = repo.split("/", 1)
    return (
        "https://api.github.com/repos/"
        f"{urllib.parse.quote(owner, safe='')}/{urllib.parse.quote(name, safe='')}/commits/"
        f"{urllib.parse.quote(branch, safe='')}"
    )


def changed_status(mode: str) -> tuple[str, bool]:
    if mode in ADVISORY_MODES:
        return "advisory-update", False
    return "update-available", True


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare pinned upstream commits with GitHub branches.")
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--allow-offline", action="store_true", help="Return success when network access is unavailable.")
    parser.add_argument(
        "--fail-on-advisory",
        action="store_true",
        help="Also return exit code 1 for methodology-advisory sources such as P2P.",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    if not 0.1 <= args.timeout <= 60:
        raise SystemExit("--timeout must be between 0.1 and 60 seconds")

    root = Path(args.root).resolve()
    try:
        manifest = json.loads((root / "UPSTREAM_SOURCES.json").read_text(encoding="utf-8"))
        sources = manifest["sources"]
        if not isinstance(sources, list):
            raise ValueError("sources must be an array")
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"invalid upstream manifest: {exc}") from exc

    results: list[dict[str, object]] = []
    offline = False
    for raw_source in sources:
        try:
            source_id, repo, branch, pinned, mode = valid_source(raw_source)
        except ValueError as exc:
            raise SystemExit(f"invalid upstream manifest: {exc}") from exc
        url = commit_url(repo, branch)
        try:
            payload = request_json(url, args.timeout)
            latest = payload.get("sha")
            if not isinstance(latest, str) or not SHA_RE.fullmatch(latest):
                raise ValueError("GitHub response has no valid commit SHA")
            if latest == pinned:
                status, actionable = "current", False
            else:
                status, actionable = changed_status(mode)
            result: dict[str, object] = {
                "id": source_id,
                "repository": repo,
                "branch": branch,
                "pinned": pinned,
                "latest": latest,
                "status": status,
                "tracking_mode": mode,
                "actionable": actionable,
            }
            if mode in ADVISORY_MODES and status == "advisory-update" and isinstance(raw_source, dict):
                result["default_action"] = raw_source.get("default_action", "ignore-unless-methodology-relevant")
                result["ignored_by_default"] = raw_source.get("ignored_by_default", [])
            results.append(result)
        except (OSError, TimeoutError, urllib.error.URLError, json.JSONDecodeError, UnicodeDecodeError, TypeError, ValueError) as exc:
            offline = True
            results.append({
                "id": source_id,
                "repository": repo,
                "branch": branch,
                "pinned": pinned,
                "latest": None,
                "status": "unavailable",
                "tracking_mode": mode,
                "actionable": False,
                "error": str(exc),
            })

    if args.as_json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(
                f"{item['id']}: {item['status']} "
                f"mode={item['tracking_mode']} actionable={str(item['actionable']).lower()} "
                f"pinned={item['pinned']} latest={item.get('latest') or '-'}"
            )
            if item["status"] == "advisory-update":
                print("  ignored by default; review only stable methodology changes")
            if item.get("error"):
                print(f"  {item['error']}")

    if any(bool(item.get("actionable")) for item in results):
        raise SystemExit(1)
    if args.fail_on_advisory and any(item["status"] == "advisory-update" for item in results):
        raise SystemExit(1)
    if offline and not args.allow_offline:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
