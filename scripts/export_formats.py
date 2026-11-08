#!/usr/bin/env python3
"""Generator for the 4 canonical Expert Panel delivery formats.

1. agent: directory structure for AI agent hosts (Claude Code, Codex, OpenCode, Gemini CLI, etc.)
2. web-skill: clean importable ZIP for web platforms supporting skill upload (Claude.ai Custom Skills, ChatGPT Workspace)
3. universal-zip: ZIP with INSTRUCTIONS.md + HOW_TO_USE.md + KNOWLEDGE.md for chats with file attachments
4. universal-text: single self-contained Markdown file for chats without skill support or zip uploads
"""
from __future__ import annotations
import argparse, io, json, os, re, shutil, zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PAYLOAD = REPO / "skills" / "expert-panel"

VERSION = "27.3.0"
SKIP = {".git", "__pycache__", "node_modules", "dist", "build"}

def get_text_content(rel_path: str) -> str:
    p = PAYLOAD / rel_path
    if not p.is_file():
        return ""
    text = p.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5:]
    return text

def build_universal_text() -> str:
    """Build a single comprehensive instruction file containing the full workflow and practices."""
    skill_text = get_text_content("SKILL.md")
    profiles = get_text_content("references/host_profiles.md")
    roles = get_text_content("references/role_registry.md")
    cards = get_text_content("references/donor_practice_cards.md")
    orchestration = get_text_content("references/skill_orchestration.md")
    offensive = get_text_content("references/offensive_security.md")
    mentor = get_text_content("references/mentor_path.md")
    legacy = get_text_content("references/legacy_capabilities.md")

    parts = [
        f"# Expert Panel v{VERSION} — Universal Text Instructions\n",
        "> Single-file instructions for web chats and models without native skill support or zip uploads.\n"
        "> Paste this into Custom Instructions / System Prompt or attach as a single Markdown file.\n\n",
        "## Part 1: Core Workflow & Routing\n",
        skill_text.strip(),
        "\n\n---\n\n## Part 2: Host Profiles & Execution Rules\n",
        profiles.strip(),
        "\n\n---\n\n## Part 3: Role Registry & Dynamic Specialization\n",
        roles.strip(),
        "\n\n---\n\n## Part 4: Compact Practice Cards & Donor Methods\n",
        cards.strip(),
        "\n\n---\n\n## Part 5: Skill Orchestration & Priority\n",
        orchestration.strip(),
        "\n\n---\n\n## Part 6: Authorized Offensive Security (Pentest / Lab / CTF)\n",
        offensive.strip(),
        "\n\n---\n\n## Part 7: Beginner Guidance (Idea to Milestone)\n",
        mentor.strip(),
        "\n\n---\n\n## Part 8: Deep Deliberation & Adaptive Output\n",
        legacy.strip(),
        "\n"
    ]
    return "\n".join(parts)

def build_universal_zip(output_path: Path):
    """Build universal ZIP with INSTRUCTIONS.md, HOW_TO_USE.md, and KNOWLEDGE.md."""
    instructions = (
        f"# Expert Panel v{VERSION} — Chat Instructions\n\n"
        "Treat the contents of this archive as your operational instructions and domain reference.\n"
        "1. Identify the task: direct answer, focused specialist, or multi-perspective review.\n"
        "2. If no separate agent processes exist, use sequential perspectives of ONE model.\n"
        "3. Prioritize: exact installed host skill → bundled full module → compact practice card → remote reference.\n"
        "4. For security requests on authorized targets, use attacker-led exploitability verification.\n"
        "5. For beginners, guide from rough idea to a small, verifiable first milestone.\n\n"
        "Refer to `KNOWLEDGE.md` for role cards, domain methods, and output contracts.\n"
    )

    how_to_use = (
        f"# How to use Expert Panel in Web AI\n\n"
        "This archive is designed for AI web chats that support uploading or attaching ZIP files.\n\n"
        "### How to use:\n"
        "1. Attach this ZIP file (`expert-panel-universal-chat.zip`) to your chat conversation.\n"
        "2. Type your message:\n"
        "   ```text\n"
        "   Read the attached archive and follow its Expert Panel instructions for my task.\n"
        "   Task: [Describe what you want to analyze, review, build, or audit]\n"
        "   ```\n"
        "3. The AI will inspect the instructions and apply the appropriate role perspectives.\n"
    )

    knowledge = build_universal_text()

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr("INSTRUCTIONS.md", instructions.encode("utf-8"))
        zf.writestr("HOW_TO_USE.md", how_to_use.encode("utf-8"))
        zf.writestr("KNOWLEDGE.md", knowledge.encode("utf-8"))

def build_web_skill_zip(output_path: Path):
    """Build a clean importable skill ZIP for Claude.ai or ChatGPT skills upload."""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for root, dirs, files in os.walk(PAYLOAD):
            dirs[:] = [d for d in dirs if d not in SKIP]
            for file in files:
                if file.endswith((".pyc", ".zip")) or file.startswith("."):
                    continue
                p = Path(root) / file
                rel = p.relative_to(PAYLOAD)
                # Keep under root folder named 'expert-panel/' for standard skill unpackers
                arcname = f"expert-panel/{rel.as_posix()}"
                zf.write(p, arcname)

def export_format(format_name: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    if format_name == "universal-text":
        out = output_dir / "EXPERT_PANEL_INSTRUCTIONS.md"
        out.write_text(build_universal_text(), encoding="utf-8")
        return out
    elif format_name == "universal-zip":
        out = output_dir / "expert-panel-universal-chat.zip"
        build_universal_zip(out)
        return out
    elif format_name == "web-skill":
        out = output_dir / "expert-panel-web-skill.zip"
        build_web_skill_zip(out)
        return out
    elif format_name == "agent":
        # Destination is directory containing the skill folder
        out = output_dir / "expert-panel"
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(PAYLOAD, out, ignore=shutil.ignore_patterns(*SKIP, "*.pyc", "*.zip"))
        return out
    else:
        raise ValueError(f"Unknown format: {format_name}")

def main():
    p = argparse.ArgumentParser(description="Export one of the 4 Expert Panel formats")
    p.add_argument("--format", choices=["agent", "web-skill", "universal-zip", "universal-text", "all"], required=True)
    p.add_argument("--output", required=True, help="Destination directory or output file")
    args = p.parse_args()

    out_dir = Path(args.output).resolve()
    if args.format == "all":
        out_dir.mkdir(parents=True, exist_ok=True)
        for fmt in ["agent", "web-skill", "universal-zip", "universal-text"]:
            res = export_format(fmt, out_dir)
            print(f"Generated {fmt}: {res}")
    else:
        res = export_format(args.format, out_dir)
        print(f"Generated {args.format}: {res}")

if __name__ == "__main__":
    main()
