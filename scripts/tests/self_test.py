#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path


def payload_root(root: Path) -> Path:
    root = root.resolve()
    for candidate in (root, root / "skills" / "expert-panel", root / "expert-panel"):
        if (candidate / "SKILL.md").is_file(): return candidate
    raise FileNotFoundError(f"payload SKILL.md not found below {root}")

def repo_root(payload: Path) -> Path:
    return payload.parents[1] if payload.parent.name == "skills" else payload.parent

def script_path(payload: Path, name: str) -> Path:
    repo = repo_root(payload)
    candidates = (repo / "scripts" / name, repo / "scripts/tests" / name, payload / "scripts" / name)
    for candidate in candidates:
        if candidate.is_file(): return candidate
    raise FileNotFoundError(f"test utility not found: {name}")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def expect_system_exit(callback, message: str) -> None:
    try:
        callback()
    except SystemExit:
        return
    raise AssertionError(message)


def test_router(root: Path) -> None:
    router = load_module("panel_router_selftest", script_path(root,"panel_router.py"))
    long_text = "Humanize this without changing facts. " + ("Neutral sentence. " * 1000)
    got = router.route(long_text)
    assert_true(got["depth"] == "QUICK" and got["execution"] == "specialist", "long Humanizer payload escalated")
    unrelated = router.route("Summarize this:\n" + ("Neutral sentence. " * 1000))
    assert_true(unrelated["depth"] == "DIRECT", "payload length activated the panel")

    positives = {
        "Улучши этот системный промпт": "PROMPT_ENGINEER",
        "сделай текст более человечным": "HUMANIZE",
        "Проведи security audit этого проекта": "SECURITY_REVIEW",
        "Redesign this GitHub README": "README_STUDIO",
        "Проверь обновления в upstream repository": "UPSTREAM_MAINTENANCE",
    }
    for text, expected in positives.items():
        assert_true(router.route(text)["specialist_route"] == expected, f"specialist route missing: {text}")

    multi = router.route("Compare Kubernetes vs ECS for cost, security and operations")
    assert_true(
        multi["trigger"] is True and multi["execution"] == "panel" and multi["depth"] == "STANDARD",
        "multi-domain trade-off failed to activate panel",
    )
    ext_h = router.route("Use $humanizer to rewrite this text naturally.")
    assert_true(ext_h["preferred_external_skill"] == "humanizer", "Humanizer delegation target missing")
    ext_r = router.route("Use $beautify-github-readme to redesign this README.")
    assert_true(ext_r["preferred_external_skill"] == "beautify-github-readme", "README delegation target missing")

    direct_queries = (
        "Compare two strings in Python.",
        "Сравни числа 10 и 12.",
        "What is a security audit?",
        "Explain prompt engineering.",
        "Humanizer is a GitHub project.",
        "What is a GitHub README?",
        "What does upstream mean in Git?",
        "Forecast for Miami tomorrow?",
    )
    for text in direct_queries:
        got = router.route(text)
        assert_true(got["depth"] == "DIRECT" and got["execution"] == "direct", f"informational query over-routed: {text}: {got}")

    high = router.route("Should I invest my retirement savings in one startup?")
    assert_true(high["depth"] == "STANDARD" and high["execution"] == "panel", "high-stakes decision stayed direct")


def test_auditor(root: Path) -> None:
    auditor = load_module("audit_readme_selftest", script_path(root,"audit_readme.py"))
    with tempfile.TemporaryDirectory() as raw:
        project = Path(raw)
        assets = project / "assets"
        assets.mkdir()
        safe_svg = assets / "safe.svg"
        safe_svg.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 30">'
            '<title>Safe diagram</title><desc>A simple rectangle.</desc><rect width="100" height="30"/></svg>',
            encoding="utf-8",
        )
        readme = project / "README.md"
        readme.write_text("![Safe diagram][hero]\n\n[hero]: assets/safe.svg\n", encoding="utf-8")
        findings = auditor.audit_readme(readme, project)
        assert_true(not findings, f"safe README produced findings: {findings}")

        encoded = "javascript:alert(1)"
        from urllib.parse import quote
        for _ in range(9):
            encoded = quote(encoded, safe="")
        bad_svg = assets / "bad.svg"
        bad_svg.write_text(
            '<!DOCTYPE svg><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            f'<title>Bad</title><desc>Bad.</desc><use href="{encoded}"/></svg>',
            encoding="utf-8",
        )
        readme.write_text('<img src="assets/bad.svg">\n![x](../outside.svg)\n', encoding="utf-8")
        findings = auditor.audit_readme(readme, project)
        codes = {item.code for item in findings}
        assert_true("svg-doctype-entity" in codes, "DOCTYPE was not detected")
        assert_true("unsafe-uri" in codes, "deeply encoded javascript URI was not detected")
        assert_true("readme-path-escape" in codes, "README path escape was not detected")
        assert_true("missing-alt" in codes, "missing HTML alt attribute was not detected")

        readme.write_text("```md\n![example](missing.svg)\n```\n`![inline](missing2.svg)`\n", encoding="utf-8")
        findings = auditor.audit_readme(readme, project)
        assert_true(not findings, f"non-rendered examples produced findings: {findings}")

        readme.write_text("![bad](file:///etc/passwd)\n![bad](C:\\secret.png)\n", encoding="utf-8")
        codes = {item.code for item in auditor.audit_readme(readme, project)}
        assert_true("unsupported-image-scheme" in codes, "unsupported image scheme was accepted")
        assert_true("absolute-image-path" in codes, "Windows absolute image path was accepted")

        css_escape = assets / "css-escape.svg"
        css_escape.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><title>x</title><desc>x</desc><style>.x{fill:url(../../secret.png)}</style></svg>', encoding="utf-8")
        codes = {item.code for item in auditor.audit_svg(css_escape, project)}
        assert_true("svg-path-escape" in codes, "CSS url() path escape was accepted")

        animated = assets / "animated.svg"
        animated.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><title>x</title><desc>x</desc><rect><animate attributeName="x" from="0" to="1" dur="1s"/></rect></svg>', encoding="utf-8")
        codes = {item.code for item in auditor.audit_svg(animated, project)}
        assert_true("svg-animation" in codes, "SMIL animation warning missing")

        readme.write_text('<picture><source srcset="assets/safe.svg 1x, https://example.com/x.png 2x"><img src="assets/safe.svg" alt="Safe"></picture>\n', encoding="utf-8")
        codes = {item.code for item in auditor.audit_readme(readme, project)}
        assert_true("remote-image" in codes, "remote srcset resource was not detected")


def test_motion_spec(root: Path) -> None:
    motion = load_module("render_motion_selftest", script_path(root,"render_readme_motion_gif.py"))
    valid = {
        "fps": 1,
        "duration": 0.1,
        "width": 1200,
        "colors": 128,
        "alpha_threshold": 128,
        "max_size_mb": 2,
        "transparent_color": "#ff00ff",
        "clip_to_base_alpha": False,
        "dither": "none",
        "reveals": [{"id": "hero", "axis": "x", "start": 0, "end": 0.1}],
        "layers": [],
    }
    motion.validate_spec(valid)
    unsafe = dict(valid)
    unsafe["reveals"] = [{"id": "../escape", "axis": "x", "start": 0, "end": 0.1}]
    expect_system_exit(lambda: motion.validate_spec(unsafe), "unsafe motion id was accepted")
    invalid_time = dict(valid)
    invalid_time["reveals"] = [{"id": "hero", "axis": "x", "start": 0.1, "end": 0.1}]
    expect_system_exit(lambda: motion.validate_spec(invalid_time), "invalid motion timing was accepted")
    duplicate = dict(valid)
    duplicate["reveals"] = [
        {"id": "hero", "axis": "x", "start": 0, "end": 0.1},
        {"id": "hero", "axis": "y", "start": 0, "end": 0.1},
    ]
    expect_system_exit(lambda: motion.validate_spec(duplicate), "duplicate motion ids were accepted")
    invalid_numeric = dict(valid)
    invalid_numeric["fps"] = "30"
    expect_system_exit(lambda: motion.validate_spec(invalid_numeric), "string motion numeric was accepted")


def test_four_formats(root: Path) -> None:
    exporter = load_module("export_formats_selftest", script_path(root, "export_formats.py"))
    import zipfile
    with tempfile.TemporaryDirectory() as raw:
        out = Path(raw)
        # 1. agent
        agent_dir = exporter.export_format("agent", out)
        assert_true((agent_dir / "SKILL.md").is_file(), "agent format missing SKILL.md")
        
        # 2. web-skill
        web_zip = exporter.export_format("web-skill", out)
        assert_true(web_zip.is_file(), "web-skill zip missing")
        with zipfile.ZipFile(web_zip) as zf:
            assert_true("expert-panel/SKILL.md" in zf.namelist(), "web-skill zip missing expert-panel/SKILL.md")
            
        # 3. universal-zip
        univ_zip = exporter.export_format("universal-zip", out)
        assert_true(univ_zip.is_file(), "universal-zip missing")
        with zipfile.ZipFile(univ_zip) as zf:
            names = set(zf.namelist())
            assert_true(names == {"INSTRUCTIONS.md", "HOW_TO_USE.md", "KNOWLEDGE.md"}, f"unexpected universal-zip entries: {names}")
            
        # 4. universal-text
        univ_text = exporter.export_format("universal-text", out)
        assert_true(univ_text.is_file() and univ_text.stat().st_size > 15000, "universal-text invalid")


def test_frontmatter(root: Path) -> None:
    validator = load_module("validate_skill_selftest", script_path(root,"validate_skill.py"))
    sample = "---\nname: test\ndescription: Works\nmetadata:\n  version: \"1.0.0\"\n---\nBody\n"
    parsed, body = validator.parse_frontmatter(sample)
    assert_true(parsed["metadata"]["version"] == "1.0.0" and body == "Body\n", "frontmatter parsing failed")
    duplicate = "---\nname: one\nname: two\ndescription: x\n---\nBody\n"
    try:
        validator.parse_frontmatter(duplicate)
    except Exception:
        pass
    else:
        raise AssertionError("duplicate YAML key was accepted")


def test_security_prompt(root: Path) -> None:
    text = (root / "references/security_review_prompt.md").read_text(encoding="utf-8")
    assert_true("Security Review: attacker-led coverage profile" in text, "security review profile title missing")
    assert_true("entry point → attacker-controlled" in text, "attacker-led flow missing")


def test_metadata_and_packaging(root: Path) -> None:
    validator = load_module("validate_skill_metadata_selftest", script_path(root,"validate_skill.py"))
    errors = validator.validate_openai_metadata(repo_root(root) / "skills")
    assert_true(not errors, f"OpenAI metadata invalid: {errors}")
    installer = load_module("installer_selftest", script_path(root,"universal_installer.py"))
    assert_true(installer.safe_name("expert-panel/SKILL.md"), "safe path rejected by installer")
    assert_true(not installer.safe_name("../escape"), "unsafe path accepted by installer")
    upstream = load_module("check_upstream_selftest", script_path(root,"check_upstream.py"))
    assert_true(upstream.commit_url("owner/repo", "feature/test").endswith("/commits/feature%2Ftest"), "upstream branch was not URL-encoded")
    manifest = json.loads((repo_root(root) / "docs/UPSTREAM_SOURCES.json").read_text(encoding="utf-8"))
    p2p = next(item for item in manifest["sources"] if item["id"] == "p2p-4pda-edition")
    assert_true(p2p.get("tracking_mode") == "methodology-advisory", "P2P tracking mode is not advisory-only")
    assert_true(upstream.changed_status("methodology-advisory") == ("advisory-update", False), "P2P advisory changes became actionable")
    assert_true(upstream.changed_status("specialist-integration") == ("update-available", True), "specialist changes stopped being actionable")
    ignored = p2p.get("ignored_by_default")
    assert_true(isinstance(ignored, list) and len(ignored) >= 5, "P2P default-ignore categories are incomplete")


def test_eval_harness(root: Path) -> None:
    runner = load_module("run_evals_selftest", script_path(root,"run_evals.py"))
    assert_true(runner.materialize_prompt({"prompt": "x", "repeat": {"text": "y", "count": 2}}) == "xyy", "valid repeat failed")
    for case in (
        {"prompt": "x", "repeat": {"text": "y", "count": -1}},
        {"prompt": "x", "repeat": {"text": "y", "count": 10001}},
        {"prompt": "x", "repeat": {"text": "y", "count": True}},
    ):
        try:
            runner.materialize_prompt(case)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid eval repeat accepted: {case}")



def test_release_audit(root: Path) -> None:
    release_audit = load_module("audit_release_selftest", script_path(root,"audit_release.py"))
    assert_true(not release_audit.audit(repo_root(root)), "clean release tree failed leak audit")
    with tempfile.TemporaryDirectory() as raw:
        sample = Path(raw)
        (sample / "skills/expert-panel").mkdir(parents=True)
        (sample / "skills/expert-panel/SKILL.md").write_text("---\nname: expert-panel\ndescription: x\n---\n", encoding="utf-8")
        (sample / "docs").mkdir()
        (sample / "scripts").mkdir()
        (sample / "README.md").write_text("ok", encoding="utf-8")
        (sample / "README_RU.md").write_text("ok", encoding="utf-8")
        assert_true(not release_audit.audit(sample), "minimal allowed tree failed audit")

        (sample / "AGENTS.md").write_text("local instructions", encoding="utf-8")
        assert_true(any("outside skills/docs/scripts" in error for error in release_audit.audit(sample)), "AGENTS.md was not blocked")
        (sample / "AGENTS.md").unlink()

        private_header = "-----BEGIN " + "PRIVATE KEY-----"
        (sample / "docs/leak.md").write_text(private_header + "\nabc\n", encoding="utf-8")
        assert_true(any("private key" in error for error in release_audit.audit(sample)), "private key was not detected")
        (sample / "docs/leak.md").write_text("token ghp_" + "A" * 35, encoding="utf-8")
        assert_true(any("GitHub token" in error for error in release_audit.audit(sample)), "GitHub token was not detected")
        (sample / "docs/leak.md").unlink()

        (sample / "notes.txt").write_text("not public", encoding="utf-8")
        assert_true(any("outside skills/docs/scripts" in error for error in release_audit.audit(sample)), "unknown root file was not blocked")


def test_public_documentation(root: Path) -> None:
    readme = (repo_root(root) / "README.md").read_text(encoding="utf-8")
    readme_ru = (repo_root(root) / "README_RU.md").read_text(encoding="utf-8")
    security = (repo_root(root) / "docs/SECURITY.md").read_text(encoding="utf-8")
    notice = (repo_root(root) / "docs/NOTICE.md").read_text(encoding="utf-8")
    for heading in ("## What is a skill?", "## Quick start", "## 4 Delivery Formats", "## Important limitations"):
        assert_true(heading in readme, f"beginner-facing English README section missing: {heading}")
    for heading in ("## Что такое скилл", "## Быстрый старт", "## 4 формата поставки", "## Важные ограничения"):
        assert_true(heading in readme_ru, f"beginner-facing Russian README section missing: {heading}")
    assert_true("Python and local scripts are not required" in readme, "English README does not explain the no-Python path")
    assert_true("git clone https://github.com/jecky5675/expert-panel.git" in readme.casefold(), "README lacks GitHub installation path")
    assert_true("ask your ai agent to install it" in readme.casefold(), "README lacks AI-agent installation path")
    assert_true("Python и запуск скриптов не требуются" in readme_ru, "Russian README does not explain the no-Python path")
    assert_true("git clone https://github.com/jecky5675/expert-panel.git" in readme_ru.casefold(), "Russian README lacks GitHub installation path")
    assert_true("попросите ии-агента установить скилл" in readme_ru.casefold(), "Russian README lacks AI-agent installation path")
    assert_true("does not guarantee" in readme.casefold(), "English README verification limits are missing")
    assert_true("не гарантирует" in readme_ru.casefold(), "Russian README verification limits are missing")
    assert_true("README_RU.md" in readme and "README.md" in readme_ru, "README language-switch links are missing")
    assert_true("Install the Expert Panel skill from" in readme, "English README lacks AI-agent installation prompt")
    assert_true("Установи скилл Expert Panel из" in readme_ru, "Russian README lacks AI-agent installation prompt")
    assert_true("P2P-4PDA-edition" in notice and "License: MIT" in notice, "P2P attribution/license is incomplete")
    inventory = json.loads((repo_root(root) / "docs/DONOR_INVENTORY.json").read_text(encoding="utf-8"))
    assert_true(len(inventory.get("bundles", [])) >= 30, "donor inventory is incomplete")
    assert_true("EXPERT_PANEL_COMPLETE.txt" not in readme and "EXPERT_PANEL_COMPLETE.txt" not in readme_ru, "README still advertises the removed duplicate TXT edition")


def test_skill_composition(root: Path) -> None:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    composition = (root / "references/skill_composition.md").read_text(encoding="utf-8")
    combined = (skill + composition).casefold()
    for token in ("humanizer", "beautify-github-readme", "do not then re-run", "generic web chats", "explicit_call", "auto_composed", "no_positive_signal"):
        assert_true(token.casefold() in combined, f"composition invariant missing: {token}")
    changelog = (repo_root(root) / "docs/CHANGELOG.md").read_text(encoding="utf-8")
    versions = __import__("re").findall(r"^## (\d+\.\d+\.\d+)\b", changelog, __import__("re").MULTILINE)
    assert_true(len(versions) == len(set(versions)), "duplicate changelog versions remain")



def test_safety_compatibility(root: Path) -> None:
    safety = (root / "references/safety_compatibility.md").read_text(encoding="utf-8").casefold()
    skill = (root / "SKILL.md").read_text(encoding="utf-8").casefold()
    prompt = (root / "references/prompt_engineering.md").read_text(encoding="utf-8").casefold()
    security = (root / "references/security_review_prompt.md").read_text(encoding="utf-8").casefold()
    humanizer = (root / "references/style_and_humanization.md").read_text(encoding="utf-8").casefold()
    exporter = load_module("export_formats_selftest", script_path(root, "export_formats.py"))
    universal_prompt = exporter.build_universal_text().casefold()
    for token in ("preserve the safe objective", "no safeguard evasion", "authorization is required", "transparent editing", "safe prompt engineering"):
        assert_true(token in safety, f"safety boundary missing: {token}")
    assert_true("safety_compatibility.md" in skill and "preserve safe utility" in skill, "SKILL.md safety boundary missing")
    for token in ("bypass safeguards", "hidden prompts", "unauthorized access", "harmless placeholders"):
        assert_true(token in prompt, f"prompt safety invariant missing: {token}")
    for token in ("explicitly authorized", "mask actual secrets", "exploit"):
        assert_true(token in security, f"security safety invariant missing: {token}")
    for token in ("conceal provenance", "impersonate", "evade ai/plagiarism detection"):
        assert_true(token in humanizer, f"humanizer safety invariant missing: {token}")
    assert_true("preserve safe utility" in universal_prompt, "universal prompt lost safety boundary")



def test_knowledge_base(root: Path) -> None:
    import json
    catalog_path = root / "knowledge/catalog.json"
    assert_true(catalog_path.is_file(), "knowledge/catalog.json missing")
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    entries = catalog.get("entries")
    assert_true(isinstance(entries, list) and len(entries) >= 10, "knowledge catalog too small")
    ids = [e["id"] for e in entries]
    assert_true(len(ids) == len(set(ids)), "duplicate knowledge ids")
    for e in entries:
        assert_true(str(e.get("url", "")).startswith("https://"), f"non-https knowledge url: {e.get('id')}")
        assert_true(isinstance(e.get("tags"), list) and e.get("domain"), f"incomplete knowledge entry: {e.get('id')}")
    index = (root / "knowledge/INDEX.md").read_text(encoding="utf-8")
    assert_true("catalog.json" in index and "not" in index.casefold(), "INDEX.md incomplete")
    protocol = (root / "references/knowledge_base.md").read_text(encoding="utf-8")
    assert_true("KB-" in protocol and "catalog" in protocol.casefold(), "knowledge_base protocol incomplete")
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    assert_true("knowledge_base.md" in skill and "Knowledge links before invention" in skill, "SKILL.md missing knowledge integration")


def test_unified_roles(root: Path) -> None:
    planner = load_module("role_orchestrator_selftest", script_path(root,"role_orchestrator.py"))
    count, failures = planner._check_cases(root / "evals/role_orchestrator_cases.json")
    assert_true(count >= 15 and not failures, f"role planner scenarios failed: {failures}")
    review = planner.orchestrate("Review my Python and React project architecture and security for an authorized pentest.")
    assert_true(any(role["layer"] == "dynamic" for role in review["roles"]), "dynamic roles were not generated")
    assert_true(any(role["id"] == "authorized_attack_hunter" for role in review["roles"]), "offensive hunter role missing")
    direct = planner.orchestrate("Что такое экспертная панель?")
    assert_true(direct["intent"] == "direct" and not direct["roles"], "informational query created a panel")
    scenarios = json.loads((root / "evals/behavioral_review_cases.json").read_text(encoding="utf-8"))
    for case in scenarios:
        routed = planner.orchestrate(case["prompt"])
        expected = case["route"]
        assert_true(routed["route"] == expected or (expected == "DIRECT" and routed["intent"] == "direct"), f"behavioral scenario route failed: {case['id']}: {routed['route']}")
        assert_true(bool(case["manual_review"]), f"manual review criteria missing: {case['id']}")
    exporter = load_module("export_formats_selftest", script_path(root, "export_formats.py"))
    text_content = exporter.build_universal_text()
    for token in ("role_orchestration.md", "mentor_path.md", "role_registry.md", "host_profiles.md", "skill_orchestration.md", "donor_practice_cards.md", "legacy_capabilities.md"):
        assert_true(token in text_content, f"universal text prompt missing section reference: {token}")


def test_distribution_profiles(root: Path) -> None:
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    profiles = (root / "references/host_profiles.md").read_text(encoding="utf-8")
    assert_true("references/host_profiles.md" in skill, "host profile reference missing in SKILL.md")
    assert_true("sequential perspective passes" in profiles and "must not claim independent agents" in profiles, "web profile lacks honest one-model boundary")
    assert_true("real subagent delegation" in profiles and "read-only by default" in profiles, "agent profile lacks delegation boundaries")
    combined = (skill + profiles + (root / "references/role_registry.md").read_text(encoding="utf-8") + (root / "references/expert_roles.md").read_text(encoding="utf-8") + (root / "references/legacy_capabilities.md").read_text(encoding="utf-8")).casefold()
    removed_role_terms = ("eth" + "ics / safety", "eth" + "ics / affected parties", "scr" + "ibe intent")
    for forbidden in removed_role_terms:
        assert_true(forbidden not in combined, f"removed role remains: {forbidden}")
    for rel in ("vendor/methodweft/entry-and-mentoring.md", "vendor/research-first-builder/SKILL.md", "vendor/security-audit/SKILL.md", "references/specialist_registry.json", "references/skill_orchestration.md", "references/donor_practice_cards.md", "references/offensive_security.md", "references/packs/manifest.json"):
        assert_true((root / rel).is_file(), f"vendored/orchestration file missing: {rel}")
    for rel in ("beautify-github-readme-MIT.txt", "humanizer-MIT.txt", "methodweft-MIT.txt", "p2p-4pda-edition-MIT.txt", "research-first-builder-MIT.txt", "security-audit-MIT.txt"):
        assert_true((repo_root(root) / "docs/licenses" / rel).is_file(), f"license notice missing: {rel}")
    inventory = json.loads((repo_root(root) / "docs/DONOR_INVENTORY.json").read_text(encoding="utf-8"))
    assert_true(len(inventory.get("bundles", [])) >= 30, "donor inventory incomplete")
    installer = script_path(root,"universal_installer.py")
    with tempfile.TemporaryDirectory() as raw:
        target_root = Path(raw) / "skills"
        import subprocess
        result = subprocess.run([sys.executable, str(installer), "--source", str(repo_root(root)), "--target", "generic", "--dest", str(target_root), "--dry-run"], capture_output=True, text=True)
        assert_true(result.returncode == 0 and not target_root.exists(), "universal installer dry-run failed")


TESTS = (
    test_distribution_profiles,
    test_unified_roles,
    test_router,
    test_auditor,
    test_motion_spec,
    test_four_formats,
    test_frontmatter,
    test_security_prompt,
    test_metadata_and_packaging,
    test_eval_harness,
    test_release_audit,
    test_public_documentation,
    test_skill_composition,
    test_safety_compatibility,
    test_knowledge_base,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    candidate = Path(parser.parse_args().root).resolve()
    root = payload_root(candidate if (candidate / "SKILL.md").is_file() else candidate / "skills")
    failures: list[str] = []
    for test in TESTS:
        try:
            test(root)
            print("PASS", test.__name__)
        except Exception as exc:
            failures.append(f"{test.__name__}: {exc}")
            print("FAIL", test.__name__, exc)
    print(f"Self-tests: {len(TESTS) - len(failures)}/{len(TESTS)} passed")
    for failure in failures:
        print("ERROR:", failure)
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
