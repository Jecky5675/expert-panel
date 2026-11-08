#!/usr/bin/env python3
"""Install the verified OpenCode plugin bundle without overwriting user files."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SKILL_SOURCE = REPO / "skills" / "expert-panel"
RENDERER = (REPO / "scripts" / "render_host_agents.py" if (REPO / "scripts" / "render_host_agents.py").is_file() else REPO / "render_host_agents.py")
INSTALLER_VERSION = "27.3.0"
MARKER = ".expert-panel-install.json"
SKIP = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "build", "dist"}

TARGET_PLUGINS = {
    "opencode": {
        "name": "OpenCode",
        "skills_dest": Path.home() / ".config/opencode/skills",
        "agents_dest": Path.home() / ".config/opencode/agents",
        "plugins_dest": Path.home() / ".config/opencode/plugins/expert-panel.mjs",
    }
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def copy_skill(dest: Path) -> dict[str, str]:
    if dest.exists():
        raise FileExistsError(f"Refusing to overwrite existing skill directory: {dest}")
    shutil.copytree(SKILL_SOURCE, dest, ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "*.zip"))
    return {
        item.relative_to(dest).as_posix(): digest(item.read_bytes())
        for item in dest.rglob("*")
        if item.is_file() and item.name != MARKER
    }


def render_agents(dest: Path) -> dict[str, str]:
    if dest.exists() and any(dest.iterdir()):
        raise FileExistsError(f"Refusing to overwrite non-empty OpenCode agent directory: {dest}")
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("render_host_agents", RENDERER)
    if not spec or not spec.loader:
        raise RuntimeError("Cannot load host-agent renderer")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    outputs = module.render(SKILL_SOURCE, dest, "opencode")
    return {item.name: digest(item.read_bytes()) for item in outputs}


def install_plugin(target_key: str, custom_skills: Path | None = None, custom_agents: Path | None = None,
                   custom_plugin: Path | None = None, dry_run: bool = False, yes: bool = False,
                   ru: bool = False) -> dict[str, object]:
    if target_key not in TARGET_PLUGINS:
        raise ValueError(f"Unsupported plugin target: {target_key}. OpenCode is the only verified native plugin profile.")
    cfg = TARGET_PLUGINS[target_key]
    skill_dest = (custom_skills or cfg["skills_dest"]).expanduser().resolve() / "expert-panel"
    agents_dest = (custom_agents or cfg["agents_dest"]).expanduser().resolve()
    plugin_dest = (custom_plugin or cfg["plugins_dest"]).expanduser().resolve()
    plugin_source = HERE / "opencode" / "index.mjs"

    if dry_run:
        return {"mode": "dry-run", "profile": "PLUGIN", "target": target_key,
                "skill": str(skill_dest), "agents": str(agents_dest), "plugin": str(plugin_dest)}
    if not yes and (not sys.stdin.isatty() or input("Confirm OpenCode plugin install? [y/N]: ").strip().casefold() not in {"y", "yes", "д", "да"}):
        return {"mode": "cancelled", "target": target_key}
    if plugin_dest.exists() or skill_dest.exists() or (agents_dest.exists() and any(agents_dest.iterdir())):
        raise FileExistsError("Installation requires empty skill, agent, and plugin destinations; no overwrite or merge is performed")

    made: list[Path] = []
    try:
        skill_dest.parent.mkdir(parents=True, exist_ok=True)
        files = copy_skill(skill_dest)
        made.append(skill_dest)
        agent_files = render_agents(agents_dest)
        made.append(agents_dest)
        plugin_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(plugin_source, plugin_dest)
        made.append(plugin_dest)
        marker = {
            "installer": INSTALLER_VERSION, "skill": "expert-panel", "profile": "PLUGIN",
            "plugin_target": target_key, "skill_path": str(skill_dest), "agents_path": str(agents_dest),
            "plugin_path": str(plugin_dest), "files": files, "agent_files": agent_files,
            "plugin_files": {plugin_dest.name: digest(plugin_dest.read_bytes())},
        }
        (skill_dest / MARKER).write_text(json.dumps(marker, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        for path in reversed(made):
            if path.is_dir(): shutil.rmtree(path, ignore_errors=True)
            else: path.unlink(missing_ok=True)
        raise
    return {"mode": "installed", "profile": "PLUGIN", "target": target_key,
            "skill": str(skill_dest), "agents": str(agents_dest), "plugin": str(plugin_dest),
            "agents_count": len(agent_files)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, choices=sorted(TARGET_PLUGINS))
    parser.add_argument("--skills-dest")
    parser.add_argument("--agents-dest")
    parser.add_argument("--plugin-dest")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true")
    parser.add_argument("--lang", choices=["ru", "en"], default="en")
    args = parser.parse_args()
    result = install_plugin(args.target,
        Path(args.skills_dest) if args.skills_dest else None,
        Path(args.agents_dest) if args.agents_dest else None,
        Path(args.plugin_dest) if args.plugin_dest else None,
        args.dry_run, args.yes, args.lang == "ru")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, PermissionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
