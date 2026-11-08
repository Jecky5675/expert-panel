#!/usr/bin/env python3
"""Render portable Expert Panel role manifests into host-native Markdown agents."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAYLOAD = HERE.parent / "skills" / "expert-panel"

HOSTS = {"opencode", "claude-code"}


def load_agents(source: Path) -> list[dict[str, object]]:
    agents: list[dict[str, object]] = []
    for path in sorted((source / "agents").glob("expert-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("id"), str):
            raise ValueError(f"Invalid agent manifest: {path}")
        agents.append(data)
    if not agents:
        raise ValueError(f"No Expert Panel agent manifests found below {source}")
    return agents


def frontmatter(agent: dict[str, object], host: str) -> str:
    description = str(agent.get("description", "Expert Panel specialist."))
    permissions = agent.get("permissions", {})
    read_only = isinstance(permissions, dict) and permissions.get("read_only") is True
    if host == "opencode":
        permission = "edit: deny\nbash: deny\nwebfetch: deny\nwebsearch: deny"
        if not read_only:
            permission = "edit: ask\nbash: ask\nwebfetch: deny\nwebsearch: deny"
        return f"---\ndescription: {description}\nmode: subagent\npermission:\n  {permission.replace(chr(10), chr(10) + '  ')}\n---\n"
    tools = "Read, Glob, Grep" if read_only else "Read, Glob, Grep, Edit, Write"
    return f"---\nname: {agent['id']}\ndescription: {description}\ntools: {tools}\nmodel: inherit\n---\n"


def render_agent(agent: dict[str, object], host: str) -> str:
    prompt = str(agent.get("system_prompt", ""))
    return frontmatter(agent, host) + "\n" + prompt.strip() + "\n"


def render(source: Path, destination: Path, host: str, dry_run: bool = False) -> list[Path]:
    if host not in HOSTS:
        raise ValueError(f"Unsupported host: {host}")
    destination.mkdir(parents=True, exist_ok=True)
    agents = load_agents(source)
    outputs = [destination / f"{agent['id']}.md" for agent in agents]
    conflicts = [output for output in outputs if output.exists()]
    if conflicts:
        raise FileExistsError(f"Refusing to overwrite existing Expert Panel agents: {', '.join(str(item) for item in conflicts)}")
    if dry_run:
        return outputs
    destination.mkdir(parents=True, exist_ok=True)
    try:
        for agent, output in zip(agents, outputs):
            output.write_text(render_agent(agent, host), encoding="utf-8")
    except Exception:
        for output in outputs:
            output.unlink(missing_ok=True)
        raise
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, choices=sorted(HOSTS))
    parser.add_argument("--dest", required=True)
    parser.add_argument("--source", default=str(PAYLOAD))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    outputs = render(Path(args.source).resolve(), Path(args.dest).expanduser().resolve(), args.host, args.dry_run)
    print("\n".join(str(item) for item in outputs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
