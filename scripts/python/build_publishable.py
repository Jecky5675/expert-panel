from __future__ import annotations
import argparse, shutil, subprocess, sys, tempfile
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
for candidate in (HERE.parents[1], HERE.parents[0], HERE.parents[2] if len(HERE.parents) > 2 else HERE):
    if (candidate / "skills" / "expert-panel" / "SKILL.md").is_file():
        REPO = candidate
        break
VERSION = "27.3.0"

def main():
    parser=argparse.ArgumentParser(description="Build npm tarball or Python wheel in a temporary isolated copy; source stays clean")
    parser.add_argument("--target",choices=("npm","python","both"),default="both")
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    output=Path(args.output).expanduser().resolve();output.mkdir(parents=True,exist_ok=True)
    results=[]
    with tempfile.TemporaryDirectory(prefix="expert-panel-build-") as tmp:
        temp = Path(tmp)
        scripts = temp / "scripts"
        shutil.copytree(REPO / "scripts", scripts, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "package-payload", "src/expert_panel_installer/skills", "src/expert_panel_installer/licenses"))
        payload=REPO/"skills"/"expert-panel"
        if not (payload/"SKILL.md").is_file(): raise SystemExit(f"Canonical payload missing: {payload}")
        package_json=json.loads((scripts/"node/package.json").read_text(encoding="utf-8"))
        if package_json.get("version") != VERSION: raise SystemExit("npm package version does not match installer release version")
        pyproject=(scripts/"python/pyproject.toml").read_text(encoding="utf-8")
        if f'version = "{VERSION}"' not in pyproject: raise SystemExit("Python package version does not match installer release version")
        node_pkg=scripts/"node";python_pkg=scripts/"python"
        if args.target in ("npm","both"):
            stage=node_pkg/"package-payload"/"skills"/"expert-panel";stage.parent.mkdir(parents=True,exist_ok=True)
            shutil.copytree(payload,stage,ignore=shutil.ignore_patterns("__pycache__","*.pyc",".git"))
            shutil.copy2(REPO/"scripts"/"export_formats.py",node_pkg/"package-payload"/"export_formats.py")
            shutil.copytree(REPO/"docs"/"licenses",node_pkg/"package-payload"/"licenses")
            shutil.copytree(REPO/"scripts"/"plugins",node_pkg/"package-payload"/"plugins",ignore=shutil.ignore_patterns("__pycache__","*.pyc"))
            shutil.copy2(REPO/"scripts"/"render_host_agents.py", node_pkg/"package-payload"/"render_host_agents.py")
            npm_manifest=node_pkg/"package.json"
            npm_manifest=json.loads((node_pkg/"package.json").read_text(encoding="utf-8"))
            if npm_manifest.get("version") != VERSION: raise SystemExit("npm package version does not match installer release version")
            npm_cmd = shutil.which("npm") or shutil.which("npm.cmd") or "npm"
            proc = subprocess.run([npm_cmd, "pack", "--pack-destination", str(output)], cwd=node_pkg, text=True, capture_output=True, shell=sys.platform.startswith("win"))
            if proc.returncode: raise SystemExit(proc.stderr or proc.stdout)
            results.append({"target":"npm","stdout":proc.stdout.strip()})
            shutil.rmtree(node_pkg/"package-payload",ignore_errors=True)
        if args.target in ("python","both"):
            package = python_pkg/"src"/"expert_panel_installer"
            (package/"skills").mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO/"scripts"/"export_formats.py", package/"export_formats.py")
            (package/"skills"/"expert-panel").parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(payload, package/"skills"/"expert-panel", ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
            shutil.copytree(REPO/"docs"/"licenses", package/"licenses")
            shutil.copytree(REPO/"scripts"/"plugins", package/"plugins", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            shutil.copy2(REPO/"scripts"/"render_host_agents.py", package/"render_host_agents.py")
            setup_py=python_pkg/"setup.py"
            setup_py.write_text(setup_py.read_text(encoding="utf-8").replace("REPO=HERE.parents[2]","REPO=HERE.parents[3]"),encoding="utf-8")

            dist=output/"python";dist.mkdir(exist_ok=True)
            proc=subprocess.run([sys.executable,"-m","build","--wheel","--sdist","--outdir",str(dist)],cwd=python_pkg,text=True,capture_output=True)
            if proc.returncode:
                raise SystemExit(proc.stderr or proc.stdout or "Install the 'build' package to create Python release artifacts")
            results.append({"target":"python-wheel+sdist","stdout":(proc.stdout+proc.stderr).strip()})
    print("\n".join(f"{r['target']}: {r['stdout']}" for r in results))
    return 0

if __name__=="__main__": raise SystemExit(main())
