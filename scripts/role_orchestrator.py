#!/usr/bin/env python3
"""Deterministic, planning-only role selection for the unified expert panel.

This module does not call a model, inspect a project, or execute requested work.
Role cards describe analytical lenses, not independent agents or authorities.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from panel_router import route

ROLE_REGISTRY = "references/role_registry.md"
MENTOR_PATH = "references/mentor_path.md"
SPECIALIST_REGISTRY = "references/specialist_registry.json"
ORCHESTRATION_PATH = "references/skill_orchestration.md"

# Only explicit intent and subject signals are used; request length is never a
# proxy for importance. Patterns are intentionally narrow to avoid accidental
# panels for ordinary informational questions.
NOVICE = (
    r"\b(?:i(?:'m| am) (?:a )?beginner|new to coding|never coded|don't know where to start|how do i start|vague idea)\b",
    r"(?<!\w)(?:я новичок|я начинающ|не умею программировать|не знаю с чего начать|с чего начать|смутная идея)",
)
IDEA = (
    r"\b(?:idea|want to (?:build|make|create)|start a project|build an app)\b",
    r"(?<!\w)(?:иде[яюи]|хочу (?:сделать|создать|приложение|проект)|придумал проект)",
)
VAGUE_IDEA = (
    r"\b(?:i have an idea|got an idea|vague idea|not sure where to start|don't know where to start)\b",
    r"(?<!\w)(?:есть идея|смутная идея)",
)
REVIEW = (
    r"\b(?:review|audit|assess|evaluate)\s+(?:(?:my|the|our|this)\s+)?(?:project|repository|repo|architecture|system|codebase)\b",
    r"\b(?:project|architecture|system|codebase)\s+(?:review|audit|assessment)\b",
    r"\b(?:expert panel|council of experts|multi[- ]expert)\b",
    r"(?<!\w)(?:проверь|оцени|проанализируй|сделай ревью|проведи аудит)\w*\s+(?:мой |наш |этот )?(?:проект|репозиторий|архитектуру|систему|кодовую базу)",
    r"(?<!\w)(?:проверь|оцени|проанализируй|сделай ревью|проведи аудит)\w*\s+(?:безопасность|уязвимости|архитектуру|риски)\s+(?:моего |нашего |этого )?(?:проекта|репозитория|системы)",
    r"\b(?:review|audit|assess)\s+(?:the\s+)?(?:security|architecture|risks)\s+of\s+(?:my|our|this|the)\s+(?:project|repository|system)\b",
    r"(?<!\w)(?:панель экспертов|совет экспертов|экспертная панель|ревью проекта|аудит проекта)",
)
MULTI_DOMAIN = (
    r"\b(?:trade[- ]offs?|cross[- ]functional|from (?:multiple|different) perspectives)\b",
    r"(?<!\w)(?:компромисс\w*|с разных сторон|нескольк\w*\s+(?:аспект\w*|област\w*))",
)
DOMAIN_PATTERNS: dict[str, tuple[str, ...]] = {
    "security": (r"\b(?:secur\w*|vulnerab\w*|privacy|threat model)\b", r"(?<!\w)(?:безопасност\w*|уязвимост\w*|приватност\w*|угроз\w*)"),
    "architecture": (r"\b(?:architect\w*|scalab\w*|database|api design|system design)\b", r"(?<!\w)(?:архитектур\w*|масштабируемост\w*|баз\w* данных|апи)"),
    "product": (r"\b(?:product|user(?:s| experience)?|usability|ux|accessib\w*|onboarding)\b", r"(?<!\w)(?:пользоват\w*|продукт\w*|доступност\w*|интерфейс\w*)"),
    "delivery": (r"\b(?:deploy\w*|release|delivery|maintain\w*|roadmap|budget|deadline)\b", r"(?<!\w)(?:релиз\w*|внедрен\w*|срок\w*|бюджет\w*|поддержк\w*|план\w*)"),
    "research": (r"\b(?:research|sources?|evidence|fact[- ]check|literature)\b", r"(?<!\w)(?:исследован\w*|источник\w*|доказательств\w*|проверь факт\w*)"),
    "writing": (r"\b(?:readme|documentation|docs|copywriting|prompt)\b", r"(?<!\w)(?:документац\w*|текст\w*|промпт\w*)"),
    "engineering": (r"\b(?:debug\w*|bug|unit test|function|implement\w*)\b", r"(?<!\w)(?:баг\w*|ошибк\w*|функци\w*|исправ\w* код|тест\w*)"),
}
HIGH_STAKES = (
    r"\b(?:medical|legal|financial|production|irreversible|safety[- ]critical)\b",
    r"(?<!\w)(?:медицин\w*|юридическ\w*|финансов\w*|продакшн\w*|необратим\w*)",
)
APPROVAL = (
    r"\b(?:publish|deploy|delete|pay|purchase|send|push)\b",
    r"(?<!\w)(?:опубликуй|разверни|удали|оплати|купи|отправь|запушь)",
)
INFORMATION = (
    r"^\s*(?:what is|what are|explain|define|how does|как работает|что такое|объясни)\b",
)

# Stable cards; evidence and prohibitions are scopes, not claims of completed work.
ROLE_CARDS: dict[str, dict[str, Any]] = {
    "mentor": {
        "lens": "Turn an unclear beginner goal into one safe, achievable first milestone.",
        "allowed_evidence": ["User-stated goals and constraints", "Confirmed beginner experience and available tools"],
        "prohibitions": ["Assume technical prerequisites", "Present a prototype as a finished product"],
        "stop_condition": "One feasible first milestone and an explicit unanswered question are identified.",
        "reference": MENTOR_PATH,
    },
    "engineer": {
        "lens": "Investigate a bounded implementation defect or test behavior.",
        "allowed_evidence": ["Provided code and error output", "Reproducible local tests with recorded results"],
        "prohibitions": ["Execute untrusted donor code", "Claim a fix without a check"],
        "stop_condition": "A minimal cause, change, and narrow verification path are identified.",
        "reference": ROLE_REGISTRY,
    },
    "architect": {
        "lens": "Inspect component boundaries, dependencies, and alternatives.",
        "allowed_evidence": ["Provided architecture and source paths", "Reproducible interface or dependency observations"],
        "prohibitions": ["Invent repository structure", "Treat style preference as a correctness defect"],
        "stop_condition": "Every material architecture concern has a location, impact, and testable alternative.",
        "reference": ROLE_REGISTRY,
    },
    "security_reviewer": {
        "lens": "Act as an authorized attacker: find footholds, bypasses and privilege transitions, validate a minimum-impact exploit primitive, and assemble only evidence-backed attack chains.",
        "allowed_evidence": ["Owned or explicitly authorized target scope", "Source/configuration and engagement rules", "Observed PoC result from the authorized lab or test environment"],
        "prohibitions": ["Indiscriminate or third-party targeting", "Destructive denial of service or persistence beyond the engagement", "Real-user credential theft, supply-chain compromise, or covert access against the owner"],
        "stop_condition": "Each candidate is confirmed, conditional, blocked, or rejected with preconditions, observed boundary result, and a reproducible authorized check.",
        "reference": "references/offensive_security.md",
    },
    "user_advocate": {
        "lens": "Assess user tasks, accessibility, and adoption friction.",
        "allowed_evidence": ["Provided user journeys", "Observed UI states", "Documented user feedback"],
        "prohibitions": ["Invent user research", "Equate personal preference with user need"],
        "stop_condition": "Each concern maps to a user task and a checkable outcome.",
        "reference": ROLE_REGISTRY,
    },
    "implementation_lead": {
        "lens": "Sequence feasible work, dependencies, rollback, and maintenance.",
        "allowed_evidence": ["Declared resources and constraints", "Provided build or deployment evidence"],
        "prohibitions": ["Promise schedule without inputs", "Deploy or modify systems during planning"],
        "stop_condition": "A bounded next step and its prerequisite are clear.",
        "reference": ROLE_REGISTRY,
    },
    "researcher": {
        "lens": "Separate sourced facts, uncertainty, and decisions requiring fresh evidence.",
        "allowed_evidence": ["User-provided sources", "Dated, independently checked references when available"],
        "prohibitions": ["Invent citations", "Claim current verification without a source check"],
        "stop_condition": "Material unsupported claims are labeled or assigned a verification step.",
        "reference": ROLE_REGISTRY,
    },
    "editor": {
        "lens": "Check clarity, audience, accuracy, and information order in written artifacts.",
        "allowed_evidence": ["Provided text and audience", "Verified product behavior"],
        "prohibitions": ["Invent product capabilities", "Change intent without approval"],
        "stop_condition": "Requested text scope and acceptance criteria are explicit.",
        "reference": ROLE_REGISTRY,
    },
    "evidence_auditor": {
        "lens": "Challenge claim-to-source links and missing or conflicting evidence.",
        "allowed_evidence": ["Traceable supplied artifacts", "Observed results with location and date"],
        "prohibitions": ["Treat role consensus as proof", "Assert tests ran without recorded results"],
        "stop_condition": "Decision-changing claims have support or are marked unverified.",
        "reference": ROLE_REGISTRY,
    },
    "adversary": {
        "lens": "Find the strongest decision-relevant failure mode or counterexample.",
        "allowed_evidence": ["Proposed decisions", "Stated assumptions", "Reproducible counterexamples"],
        "prohibitions": ["Invent objections", "Overwrite the evidence auditor's findings"],
        "stop_condition": "One meaningful alternative or failure mode is tested, or none is found.",
        "reference": ROLE_REGISTRY,
    },
    "synthesizer": {
        "lens": "Integrate evidence and trade-offs without suppressing unresolved dissent.",
        "allowed_evidence": ["Final role findings", "Verified constraints and conflicts"],
        "prohibitions": ["Count votes as evidence", "Hide uncertainty or residual risk"],
        "stop_condition": "Decision, dissent, next check, and limitations are stated.",
        "reference": ROLE_REGISTRY,
    },
}

DOMAIN_ROLE = {
    "security": "security_reviewer",
    "architecture": "architect",
    "product": "user_advocate",
    "delivery": "implementation_lead",
    "research": "researcher",
    "writing": "editor",
    "engineering": "engineer",
}

DYNAMIC_ROLE_HINTS = {
    "python": {"id": "python_specialist", "lens": "Inspect Python runtime, typing, async boundaries, dependencies and test seams.", "question": "What is the smallest idiomatic change supported by the actual Python project?"},
    "react": {"id": "react_specialist", "lens": "Inspect component state, rendering, interaction and accessibility evidence.", "question": "Which UI state or component boundary can fail under the requested change?"},
    "next": {"id": "nextjs_specialist", "lens": "Inspect server/client boundaries, routes, data loading, caching and framework version.", "question": "What executes where, and which framework contract must remain stable?"},
    "c++": {"id": "cpp_specialist", "lens": "Inspect ownership, lifetime, ABI, toolchain and memory-safety evidence.", "question": "Which lifetime or compatibility assumption can fail in the target build?"},
    "c#": {"id": "dotnet_specialist", "lens": "Inspect target framework, async/disposal, nullable flow and API compatibility.", "question": "Which .NET contract or runtime assumption needs a focused check?"},
    "ui": {"id": "ui_quality_specialist", "lens": "Inspect user flow, hierarchy, states, responsive behavior and accessible interaction.", "question": "Which user-visible state or interaction is least supported by evidence?"},
    "database": {"id": "data_boundary_specialist", "lens": "Inspect schema, ownership, consistency, query paths and migration/recovery seams.", "question": "Which data invariant or query boundary can fail under realistic use?"},
    "mcp": {"id": "tool_boundary_specialist", "lens": "Inspect tool contracts, authentication, data flow, error handling and least privilege.", "question": "Which tool boundary could widen authority or leak data?"},
}


def dynamic_roles(request: str, domains: list[str]) -> list[dict[str, Any]]:
    text = request.casefold()
    selected: list[dict[str, Any]] = []
    for hint, card in DYNAMIC_ROLE_HINTS.items():
        if hint in text:
            selected.append({"id": card["id"], "layer": "dynamic", "lens": card["lens"], "key_question": card["question"], "allowed_evidence": ["Actual scoped artifacts and observed checks only"], "prohibitions": ["Invent stack/version or claim an external skill ran"], "stop_condition": "The stack-specific question has an evidence-backed answer or is marked UNKNOWN.", "reference": SPECIALIST_REGISTRY})
    if "security" in domains and any(word in text for word in ("pentest", "penetration", "red team", "exploit", "ctf", "лаборатор", "пентест", "эксплуат")):
        selected.append({"id": "authorized_attack_hunter", "layer": "dynamic", "lens": "Model an authorized attacker, find bypasses and validate a minimum-impact exploit primitive before claiming a chain.", "key_question": "Which trust boundary can the scoped attacker cross, under which explicit preconditions?", "allowed_evidence": ["Authorized target and engagement card", "Source/configuration and minimum-impact lab PoC"], "prohibitions": ["Third-party targeting, destructive DoS, persistence, real-user credential theft or covert access"], "stop_condition": "Every candidate is CONFIRMED, CONDITIONAL, BLOCKED or REJECTED with observed boundary evidence.", "reference": "references/offensive_security.md"})
    return selected


def _matches(text: str, patterns: tuple[str, ...]) -> bool:
    """Return whether a bounded signal matches the case-folded request."""
    return any(re.search(pattern, text, re.IGNORECASE | re.UNICODE) for pattern in patterns)


def classify_request(request: str) -> dict[str, Any]:
    """Classify intent and scope from the user's words, not external evidence.

    Args:
        request: Plain-text user request (at most 20,000 characters).

    Returns:
        Deterministic intent, domain signals, and explicit guardrails.

    Raises:
        ValueError: If request is empty or exceeds the bound.
        TypeError: If request is not text.
    """
    if not isinstance(request, str):
        raise TypeError("request must be a string")
    text = request.strip()
    if not text or len(text) > 20_000:
        raise ValueError("request must contain 1 to 20000 non-whitespace characters")
    normalized = text.casefold()
    domains = [name for name, patterns in DOMAIN_PATTERNS.items() if _matches(normalized, patterns)]
    routing = route(text)
    informational = _matches(normalized, INFORMATION)
    if not routing["trigger"]:
        intent = "direct"
    elif "PROJECT_REVIEW" in routing["overlays"] or (
        routing["execution"] == "panel" and routing["specialist_route"] is None
    ):
        intent = "project_review"
    elif routing["specialist_route"] == "BEGINNER_GUIDE":
        intent = "beginner_mentoring"
    elif routing["execution"] == "panel":
        intent = "project_review"
    else:
        intent = "focused_specialist"
    if not informational and intent == "direct" and routing["execution"] == "direct":
        if _matches(normalized, IDEA) and _matches(normalized, NOVICE) and _matches(normalized, (r"(?<!\w)помоги\w*", r"\bguide me\b")):
            intent = "beginner_mentoring"
        elif _matches(normalized, (r"(?<!\w)исправ\w*\s+баг", r"\bfix (?:a |the )?bug\b")) or (
            _matches(normalized, APPROVAL) and "writing" in domains
        ):
            intent = "focused_specialist"
    if intent == "project_review" and _matches(normalized, (r"(?<!\w)без\s+аудита\b", r"\bwithout an audit\b")):
        intent = "focused_specialist"
    return {
        "intent": intent,
        "route": routing["specialist_route"] or ("PROJECT_REVIEW" if "PROJECT_REVIEW" in routing["overlays"] else routing["execution"].upper()),
        "domains": domains,
        "high_stakes_signal": _matches(normalized, HIGH_STAKES),
        "approval_required_for_action": _matches(normalized, APPROVAL),
        "scope": {
            "goal": text,
            "known_artifacts": [],
            "assumptions_to_confirm": ["Available artifacts, constraints, and success criteria are not independently verified."],
            "out_of_scope": ["Executing user or donor code", "Making changes or publishing as part of this plan"],
        },
    }


def select_roles(classification: dict[str, Any]) -> list[dict[str, Any]]:
    """Select built-in role lenses, then add task-specific dynamic roles."""
    intent = classification["intent"]
    domains = classification["domains"]
    request = classification["scope"]["goal"]
    if intent == "direct":
        names: list[str] = []
    elif intent == "beginner_mentoring":
        names = ["mentor", "implementation_lead"]
    elif intent == "focused_specialist":
        specialist_roles = {
            "SECURITY_REVIEW": "security_reviewer",
            "README_STUDIO": "editor",
            "PROMPT_ENGINEER": "editor",
            "HUMANIZE": "editor",
            "UPSTREAM_MAINTENANCE": "researcher",
        }
        names = [specialist_roles.get(classification["route"], DOMAIN_ROLE[domains[0]] if domains else "researcher")]
    else:
        names = [DOMAIN_ROLE[name] for name in domains]
        if not names:
            names = ["architect", "user_advocate", "implementation_lead"]
        # A review needs a distinct challenge, evidence check, and synthesis.
        names = names[:4] + ["evidence_auditor", "adversary", "synthesizer"]
    built_in = [{"id": name, "layer": "built_in", **ROLE_CARDS[name]} for name in dict.fromkeys(names)]
    dynamic = dynamic_roles(request, domains)
    used = {role["id"] for role in built_in}
    return built_in + [role for role in dynamic if role["id"] not in used]


def build_stage_plan(classification: dict[str, Any], roles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Produce bounded, non-executing stages with explicit verification gates."""
    intent = classification["intent"]
    role_ids = [role["id"] for role in roles]
    stages: list[tuple[str, int, list[str], str]] = []
    if intent == "direct":
        stages = [("clarify_or_answer", 1, [], "Answer only what is supported by the request; ask for missing scope if necessary.")]
    elif intent == "beginner_mentoring":
        stages = [
            ("clarify_goal", 2, ["mentor"], "Ask at most three targeted questions; do not assume tools or experience."),
            ("first_milestone", 2, role_ids, "Propose one small reversible exercise with an observable success signal."),
            ("check_learning", 1, ["mentor"], "Confirm the learner's result before advancing; do not claim it was tested."),
        ]
    elif intent == "focused_specialist":
        stages = [
            ("scope", 1, role_ids, "Identify the exact artifact and acceptance criteria."),
            ("specialist_pass", 2, role_ids, "Use only available evidence; label missing artifacts."),
            ("verification", 1, role_ids, "Name a narrow safe check and record whether it actually ran."),
        ]
    else:
        domain_ids = [role_id for role_id in role_ids if role_id not in {"evidence_auditor", "adversary", "synthesizer"}]
        stages = [
            ("scope", 1, [], "Fix goal, boundaries, criteria, and access before review."),
            ("independent_lenses", 1, domain_ids, "Separate role passes; do not imply independent agents or verified findings."),
            ("evidence_check", 1, ["evidence_auditor"], "Trace material claims to supplied sources; mark gaps."),
            ("countercheck", 1, ["adversary"], "Challenge only decision-changing claims; stop if no new evidence or risk."),
            ("synthesis", 1, ["synthesizer"], "Preserve dissent, priorities, and unresolved questions."),
            ("verification", 1, ["evidence_auditor"], "Propose reproducible checks; report actual status separately."),
        ]
    return [
        {"phase": name, "max_passes": budget, "roles": assigned, "exit_gate": gate}
        for name, budget, assigned, gate in stages
    ]


def orchestrate(request: str) -> dict[str, Any]:
    """Return a JSON-serializable plan without reading or executing project code."""
    classification = classify_request(request)
    roles = select_roles(classification)
    limitations = [
        "Keyword routing is heuristic; ambiguous intent needs user clarification.",
        "No repository inspection, source validation, model invocation, or donor-code execution occurred.",
        "Role cards are analytical lenses, not independent reviewers or professional advice.",
    ]
    if classification["high_stakes_signal"]:
        limitations.append("High-stakes subject detected; seek qualified review before consequential decisions.")
    if classification["approval_required_for_action"]:
        limitations.append("Publishing, deployment, deletion, payment, or sending requires explicit prior approval; no action is performed here.")
    return {
        **classification,
        "roles": roles,
        "stages": build_stage_plan(classification, roles),
        "verification": {"status": "not_performed", "required": "Verify material claims against authorized evidence before reporting findings."},
        "limitations": limitations,
        "references": [ROLE_REGISTRY, MENTOR_PATH],
    }


def _check_cases(path: Path) -> tuple[int, list[str]]:
    """Check declarative expectations without executing code from the cases file."""
    cases = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty JSON array")
    failures: list[str] = []
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or not isinstance(case.get("prompt"), str) or not isinstance(case.get("expect"), dict):
            raise ValueError(f"invalid case at index {index}")
        result = orchestrate(case["prompt"])
        expected = case["expect"]
        ids = [role["id"] for role in result["roles"]]
        for key in ("intent", "domains", "high_stakes_signal", "approval_required_for_action"):
            if key in expected and expected[key] != result[key]:
                failures.append(f"{case.get('id', index)}: {key}: {result[key]!r} != {expected[key]!r}")
        for role in expected.get("roles_contain", []):
            if role not in ids:
                failures.append(f"{case.get('id', index)}: missing role {role}")
        for role in expected.get("roles_exclude", []):
            if role in ids:
                failures.append(f"{case.get('id', index)}: unexpected role {role}")
    return len(cases), failures


def main() -> None:
    """Print a plan/catalog as JSON, or check the bounded declarative case suite."""
    parser = argparse.ArgumentParser(description="Plan role lenses without executing the requested work.")
    parser.add_argument("request", nargs="?", help="User request to classify")
    parser.add_argument("--catalog", action="store_true", help="Show available role cards as JSON")
    parser.add_argument("--check-cases", action="store_true", help="Check local declarative eval cases")
    args = parser.parse_args()
    if sum((bool(args.request), args.catalog, args.check_cases)) != 1:
        parser.error("provide exactly one request, --catalog, or --check-cases")
    if args.catalog:
        result: dict[str, Any] = {"roles": ROLE_CARDS, "references": [ROLE_REGISTRY, MENTOR_PATH]}
    elif args.check_cases:
        try:
            count, failures = _check_cases(Path(__file__).resolve().parents[1] / "skills" / "expert-panel" / "evals" / "role_orchestrator_cases.json")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            parser.error(str(exc))
        result = {"passed": count - len({failure.split(":", 1)[0] for failure in failures}), "total": count, "failures": failures}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if failures:
            raise SystemExit(1)
        return
    else:
        try:
            result = orchestrate(args.request)
        except (ValueError, TypeError) as exc:
            parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
