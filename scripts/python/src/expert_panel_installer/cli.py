from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

VERSION = "27.3.0"
SKILL_NAME = "expert-panel"
TARGETS = {
    "generic": Path(".agents/skills"), "claude-code": Path(".claude/skills"),
    "codex": Path(".agents/skills"), "opencode": Path(".config/opencode/skills"),
    "gemini-cli": Path(".gemini/skills"), "openclaw": Path(".openclaw/workspace/skills"),
    "hermes": Path(".hermes/skills"),
}
SKIP = {".git", "__pycache__", "node_modules", "dist", "build"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def payload_root() -> Path:
    bundled = Path(__file__).resolve().parent / "skills" / SKILL_NAME
    if (bundled / "SKILL.md").is_file():
        return bundled
    override = os.environ.get("EXPERT_PANEL_SOURCE")
    if override:
        candidate = Path(override).expanduser().resolve()
        for payload in (candidate / "skills" / SKILL_NAME, candidate):
            if (payload / "SKILL.md").is_file():
                return payload
    raise FileNotFoundError("Bundled Expert Panel skill payload is missing; reinstall the package")


def bundled_exporter() -> Path:
    exporter = Path(__file__).resolve().parent / "export_formats.py"
    if not exporter.is_file():
        raise FileNotFoundError("Bundled format exporter is missing")
    return exporter


def bundled_plugin_installer() -> Path:
    installer = Path(__file__).resolve().parent / "plugins" / "setup_plugin.py"
    if not installer.is_file():
        raise FileNotFoundError("Bundled plugin installer is missing")
    return installer


def walk(root: Path):
    for base, dirs, names in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in SKIP and not (Path(base) / d).is_symlink())
        for name in sorted(names):
            path = Path(base) / name
            if path.is_symlink() or path.suffix in {".pyc", ".zip"}:
                continue
            yield path.relative_to(root), path.read_bytes()


def install(source: Path, root: Path, dry_run: bool, yes: bool):
    target = root.expanduser().resolve()
    target = target if target.name == SKILL_NAME else target / SKILL_NAME
    source = source.resolve()
    if target == source or source in target.parents:
        raise ValueError(f"Target cannot be source or inside source: {target}")
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Refusing to overwrite {target}")
    payload = list(walk(source))
    manifest = {"installer": VERSION, "skill": SKILL_NAME, "profile": "SOLO",
                "files": {str(rel).replace("\\", "/"): digest(data) for rel, data in payload}}
    print(f"Source: {source}\nTarget: {target}\nFiles: {len(payload)}")
    if dry_run:
        return {"mode": "dry-run", "target": str(target), "count": len(payload)}
    if not yes and input("Install? [y/N] ").strip().lower() != "y":
        return {"mode": "cancelled"}
    target.mkdir(parents=True)
    try:
        for rel, data in payload:
            out = target / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        (target / ".expert-panel-install.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    except Exception:
        shutil.rmtree(target, ignore_errors=True)
        raise
    return {"mode": "installed", "target": str(target), "count": len(payload)}


def uninstall(path: Path, yes: bool):
    target = path.expanduser().resolve()
    marker = target / ".expert-panel-install.json"
    data = json.loads(marker.read_text(encoding="utf-8"))
    if data.get("installer") != VERSION or data.get("skill") != SKILL_NAME or not isinstance(data.get("files"), dict):
        raise ValueError("Unrecognized install marker")
    for rel, expected in data["files"].items():
        item = target / rel
        if not item.is_file() or digest(item.read_bytes()) != expected:
            raise ValueError(f"Modified/missing file; refusing removal: {rel}")
    if not yes and input(f"Uninstall {target}? [y/N] ").strip().lower() != "y":
        return {"mode": "cancelled"}
    shutil.rmtree(target)
    return {"mode": "uninstalled", "target": str(target)}


def menu():
    opts = ["Install for agent host", "Export a delivery format", "Uninstall marked installation", "Exit"]
    print("\nExpert Panel installer")
    for i, option in enumerate(opts, 1):
        print(f"{i}. {option}")
    value = input("Choose: ").strip()
    if not value.isdigit() or not 1 <= int(value) <= len(opts):
        raise ValueError("Invalid menu selection")
    action = int(value) - 1
    if action == 3:
        return "exit", None
    if action == 0:
        names = list(TARGETS) + ["custom"]
        for i, name in enumerate(names, 1):
            print(f"{i}. {name}")
        value = input("Target: ").strip()
        if not value.isdigit() or not 1 <= int(value) <= len(names):
            raise ValueError("Invalid target")
        name = names[int(value) - 1]
        return "install", str(Path.home() / TARGETS[name]) if name != "custom" else input("Skills root: ").strip()
    if action == 1:
        formats = ["agent", "web-skill", "universal-zip", "universal-text"]
        for i, name in enumerate(formats, 1):
            print(f"{i}. {name}")
        value = input("Format: ").strip()
        if not value.isdigit() or not 1 <= int(value) <= len(formats):
            raise ValueError("Invalid format")
        return "export:" + formats[int(value) - 1], input("Output directory: ").strip()
    return "uninstall", input("Installed skill directory: ").strip()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Interactive universal Expert Panel installer")
    parser.add_argument("--target", choices=sorted(TARGETS))
    parser.add_argument("--dest", help="Skills root")
    parser.add_argument("--format", choices=("agent", "web-skill", "universal-zip", "universal-text"))
    parser.add_argument("--output", help="Export directory")
    parser.add_argument("--uninstall", metavar="DIR")
    parser.add_argument("--plugin", choices=("opencode", "claude-code", "zed"), help="Install a bundled client plugin")
    parser.add_argument("--skills-dest")
    parser.add_argument("--agents-dest")
    parser.add_argument("--plugin-dest")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args(argv)
    try:
        source = payload_root()
        if args.uninstall:
            result = uninstall(Path(args.uninstall), args.yes)
        elif args.plugin:
            command = [sys.executable, str(bundled_plugin_installer()), "--target", args.plugin]
            for flag, value in (("--skills-dest", args.skills_dest), ("--agents-dest", args.agents_dest), ("--plugin-dest", args.plugin_dest)):
                if value:
                    command.extend((flag, value))
            if args.dry_run:
                command.append("--dry-run")
            if args.yes:
                command.append("--yes")
            return subprocess.run(command, check=False).returncode
        elif args.format:
            if args.format == "agent":
                target = Path(args.dest).expanduser() if args.dest else Path.home() / TARGETS[args.target or "generic"]
                result = install(source, target, args.dry_run, args.yes)
            else:
                if not args.output:
                    raise ValueError("--output is required for export formats")
                proc = subprocess.run([sys.executable, str(bundled_exporter()), "--format", args.format, "--output", args.output], check=False)
                return proc.returncode
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0
        else:
            action, value = menu()
            if action == "exit":
                return 0
            if action == "install":
                result = install(source, Path(value), False, args.yes)
            elif action.startswith("export:"):
                proc = subprocess.run([sys.executable, str(bundled_exporter()), "--format", action.split(":", 1)[1], "--output", value], check=False)
                return proc.returncode
            else:
                result = uninstall(Path(value), args.yes)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
