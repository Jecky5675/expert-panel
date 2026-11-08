#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    name: str
    patterns: tuple[str, ...]


RULES = (
    Rule("SECURITY_REVIEW", (
        r"\b(?:run|perform|conduct|do|start|use)\s+(?:(?:a|an|the)\s+)?security\s+(?:audit|review|assessment)\b",
        r"\bsecurity\s+(?:audit|review|assessment)\s+(?:this|the|my|our|of)\b",
        r"\b(?:audit|review|scan)\s+(?:the\s+)?(?:source\s+)?code\s+for\s+(?:security|vulnerabilit)",
        r"\b(?:audit|review|scan)\s+(?:(?:this|the|my|our)\s+)?(?:codebase|repository|project)\s+for\s+(?:security|vulnerabilit)",
        r"\bfind\s+vulnerabilit\w*\s+in\s+(?:this\s+)?(?:code|project|app)",
        r"(?<!\w)(?:провед|сдел|выполн|запуст)\w*\s+(?:security\s+audit|аудит\w*\s+безопасност\w*)",
        r"(?<!\w)проверь\w*\s+(?:этот\s+)?(?:код|проект|приложен\w*)\s+на\s+уязвимост\w*",
        r"(?<!\w)найд\w*\s+уязвимост\w*\s+в\s+(?:коде|проекте|приложен\w*)",
    )),
    Rule("SECURITY", (
        r"\bsecurity\b", r"\bvulnerabilit\w*\b", r"\bthreat\w*\b", r"\bprivacy\b",
        r"(?<!\w)безопас\w*", r"(?<!\w)уязв\w*", r"(?<!\w)мошенн\w*",
    )),
    Rule("AUDIT", (
        r"\baudit\b", r"\bdue\s+diligence\b", r"\bcompliance\s+(?:review|assessment)\b",
        r"\b(?:architecture|design|implementation|code)\s+review\b",
        r"(?<!\w)аудит\w*", r"(?<!\w)ревью\w*\s+(?:архитектур\w*|код\w*|проекта|систем\w*)",
        r"(?<!\w)проверк\w*\s+(?:соответств\w*|архитектур\w*|реализац\w*)",
    )),
    Rule("VERIFY", (
        r"\bverify\b", r"\bfact[- ]?check\w*\b", r"\bcurrent\b", r"\blatest\b", r"\bevidence\b",
        r"(?<!\w)актуальн\w*", r"(?<!\w)проверь\s+факт\w*", r"(?<!\w)верифиц\w*",
    )),
    Rule("PLAN", (
        r"\bplan(?:ning)?\b", r"\broadmap\b", r"\bstrategy\b", r"\bimplementation\s+plan\b",
        r"(?<!\w)план\w*", r"(?<!\w)стратег\w*", r"(?<!\w)дорожн\w*\s+карт\w*",
    )),
    Rule("IDEATE", (
        r"\bbrainstorm\w*\b", r"\bidea(?:s|tion)?\b", r"\bcreative\s+directions?\b",
        r"(?<!\w)иде[яи]\w*", r"(?<!\w)мозгов\w*\s+штурм\w*",
    )),
    Rule("CRITIQUE", (
        r"\b(?:critique|criticize|challenge|stress[- ]test)\w*\b",
        r"\b(?:review|evaluate)\s+(?:this|the|my|our)\s+(?:proposal|draft|design|plan)\b",
        r"(?<!\w)(?:раскритикуй|покритикуй|оспорь)\w*",
        r"(?<!\w)(?:разбери|проверь)\w*\s+(?:слабые\s+места|недостатки|предложение|план|дизайн)",
    )),
    Rule("DECISION", (
        r"\b(?:help\s+me\s+)?(?:decide|choose|pick)\b",
        r"\bwhich\s+(?:option|approach|alternative)\s+(?:should|would)",
        r"(?<!\w)(?:помоги\w*\s+)?(?:выбрат|решит)\w*",
        r"(?<!\w)что\s+(?:лучше|выгоднее|предпочтительнее)\s+выбрат",
    )),
    Rule("PRE_MORTEM", (
        r"\bassume\s+(?:the\s+)?(?:plan|launch|project)\s+failed\b",
        r"\bwhat\s+could\s+go\s+wrong\b", r"\bfailure\s+scenarios?\b",
        r"(?<!\w)представь\w*\s*,?\s*что\s+план\s+провалил\w*",
        r"(?<!\w)что\s+может\s+пойти\s+не\s+так",
    )),
    Rule("LEARN", (
        r"\b(?:teach|explain\s+to\s+me|walk\s+me\s+through|help\s+me\s+learn)\b",
        r"\b(?:i am|i'm)\s+(?:a\s+)?(?:beginner|new\s+to)",
        r"(?<!\w)(?:научи|обучи|объясни\s+мне|проведи\s+меня\s+по\s+шагам)",
        r"(?<!\w)я\s+(?:новичок|начинающ\w*)",
    )),
    Rule("FORECAST", (
        r"\bforecast\w*\b", r"\bfuture\s+scenarios?\b", r"\bscenario\s+planning\b",
        r"(?<!\w)прогноз\w*", r"(?<!\w)сценарн\w*\s+(?:анализ|планирован)\w*",
    )),
    Rule("MEDIATE", (
        r"\bmediat\w*\b", r"\bconflict\s+resolution\b", r"\bnegotiat\w*\b",
        r"(?<!\w)медиац\w*", r"(?<!\w)разреш\w*\s+конфликт\w*", r"(?<!\w)переговор\w*",
    )),
    Rule("RESEARCH", (
        r"\bliterature\s+review\b", r"\bresearch\s+synthesis\b", r"\bdeep\s+research\b",
        r"\bsystematic\s+review\b", r"(?<!\w)глубок\w*\s+исследован\w*",
        r"(?<!\w)обзор\w*\s+литератур\w*", r"(?<!\w)синтез\w*\s+исследован\w*",
    )),
    Rule("PROMPT_ENGINEER", (
        r"\b(?:use|apply|run|invoke)\s+(?:the\s+)?prompt\s+engineer(?:ing)?\b",
        r"\b(?:create|write|improve|rewrite|audit|review|optimi[sz]e|adapt|refactor)\w*\s+(?:this\s+|the\s+|a\s+)?(?:system\s+|developer\s+)?prompt\b",
        r"\b(?:create|write|improve|rewrite|audit|review|optimi[sz]e|adapt|refactor)\w*\s+(?:these\s+|the\s+)?agent\s+instructions?\b",
        r"(?<!\w)(?:созд|напиш|улучш|перепиш|проверь|оптимиз|адаптир)\w*\s+(?:(?:этот|данн\w*)\s+)?(?:системн\w*\s+)?промпт\w*",
        r"(?<!\w)(?:используй|примени|запусти)\w*\s+промпт[- ]?инженер\w*",
    )),
    Rule("HARNESS", (
        r"\bai\s+agent\b", r"\bagent\s+harness\b", r"\btool\s+calling\b", r"\bcontext\s+engineering\b",
        r"\bmcp\b", r"\bagent\s+memory\b", r"(?<!\w)ии[- ]?агент\w*", r"(?<!\w)mcp[- ]?сервер\w*",
        r"(?<!\w)контекстн\w*\s+инженер\w*", r"(?<!\w)памят\w*\s+агент\w*",
    )),
    Rule("UPSTREAM_MAINTENANCE", (
        r"\b(?:use|run|invoke)\s+(?:the\s+)?upstream\s+maintenance\b", r"\bcheck\s+(?:for\s+)?updates?\s+(?:in|from|for)\s+(?:the\s+)?(?:upstream\s+)?repo(?:sitory)?\b",
        r"\bmerge\s+(?:the\s+)?latest\s+(?:upstream\s+)?changes\b",
        r"\bsync\s+with\s+(?:the\s+)?(?:upstream|repository)\b",
        r"(?<!\w)проверь\w*\s+обновлен\w*\s+(?:в|из|для)\s+(?:(?:upstream\s+)?(?:репозитор\w*|repository)|github|upstream)",
        r"(?<!\w)обнови\w*\s+(?:скилл|модул\w*)\s+из\s+репозитор\w*",
        r"(?<!\w)сверь\w*\s+(?:с|со)\s+upstream",
    )),
    Rule("HUMANIZE", (
        r"(?<!\w)\$humanizer\b", r"\b(?:use|run|apply|invoke)\s+(?:the\s+)?humanizer\b", r"\bhumanize(?!r)\w*\b", r"\bhumanization\b", r"\bde[- ]?ai\b", r"\bnaturalize\b", r"\bremove\s+ai[- ]writing\b",
        r"\bmake\s+(?:this|it|the\s+text)\s+(?:sound\s+)?(?:more\s+)?(?:human|natural|human[- ]like)\b",
        r"\bmake\s+(?:this|it|the\s+text)\s+(?:more\s+)?(?:human|natural|human[- ]like)\b",
        r"(?<!\w)гуманиз\w*", r"(?<!\w)очеловеч\w*", r"(?<!\w)убер\w*\s+(?:шаблон\w*\s+)?ии[- ]?стил\w*",
        r"(?<!\w)де[- ]?ии\b", r"(?<!\w)де[- ]?ai\b",
        r"(?<!\w)(?:сделай|перепиш)\w*\s+(?:этот\s+|данн\w*\s+)?текст\w*\s+(?:естествен\w*|жив\w*|человечн\w*)",
        r"(?<!\w)(?:сделай|перепиш)\w*\s+(?:текст\w*\s+)?(?:более\s+)?(?:естествен\w*|человечн\w*|жив\w*)",
        r"(?<!\w)более\s+человечн\w*",
    )),
    Rule("README_STUDIO", (
        r"(?<!\w)\$beautify-github-readme\b", r"\b(?:use|run|apply|invoke)\s+(?:the\s+)?beautify-github-readme\b", r"\bbeautif\w*\s+(?:the\s+)?readme\b",
        r"\b(?:need|want)\s+(?:a|the)\s+(?:github\s+)?readme\b",
        r"\b(?:create|write|redesign|audit|improve|update|rebrand|simplify)\w*\s+(?:(?:the|a|this|my|our)\s+)?(?:github\s+)?readme\b",
        r"\breadme\s+(?:hero|badge|svg|gif|banner|diagram|asset|homepage)\b", r"\brepository\s+homepage\b",
        r"\b(?:svg|png|webp)\s+(?:hero|badge|banner)\b.*\breadme\b",
        r"\breadme\b.*\b(?:svg|png|webp)\s+(?:hero|badge|banner)\b",
        r"(?<!\w)(?:созд|напиш|оформ|улучш|обнов|переработ|редизайн|аудит)\w*\s+(?:github\s+)?readme",
        r"(?<!\w)(?:герой|баннер|бейдж|диаграмм)\w*\s+(?:для\s+)?readme",
    )),
)

EXPLICIT_PANEL = (
    r"\bexpert\s+panel\b", r"\bcouncil\s+of\s+experts\b", r"\bask\s+the\s+experts\b", r"\bmulti[- ]expert\b",
    r"(?<!\w)панел\w*\s+эксперт\w*", r"(?<!\w)совет\w*\s+эксперт\w*", r"(?<!\w)экспертн\w*\s+мнени\w*",
)

HIGH_RISK = (
    r"\blegal\b", r"\bmedical\b", r"\bfinancial\b", r"\bsafety[- ]critical\b", r"\bproduction\b",
    r"\bregulat\w*\b", r"\binvest(?:ment|ing)?\b", r"\bretirement\b", r"\bmedicat\w*\b",
    r"\bprescription\b", r"\birreversible\b", r"\bmission[- ]critical\b",
    r"(?<!\w)закон\w*", r"(?<!\w)медиц\w*", r"(?<!\w)лекарств\w*", r"(?<!\w)лечен\w*",
    r"(?<!\w)финанс\w*", r"(?<!\w)пенси\w*", r"(?<!\w)продакш\w*",
    r"(?<!\w)необратим\w*", r"(?<!\w)критическ\w*\s+важн\w*",
)

DEEP_MARKERS = (
    r"\bresearch[- ]grade\b", r"\bcomprehensive\b", r"\bexhaustive\b", r"\bdeep\s+(?:audit|analysis|review|research)\b",
    r"\bcross[- ]jurisdiction\b", r"(?<!\w)исчерпывающ\w*", r"(?<!\w)комплексн\w*\s+(?:аудит|исследован|анализ)\w*",
    r"(?<!\w)глубок\w*\s+(?:аудит|исследован|анализ)\w*",
)

COMPARISON_MARKERS = (
    r"\bcompare\b", r"\bversus\b", r"\bvs\.?\b", r"(?<!\w)сравн\w*",
)

TRADEOFF_MARKERS = (
    r"\btrade[- ]?off\w*\b", r"\bmultiple\s+domains?\b", r"\bcross[- ]functional\b",
    r"\barchitecture\s+decision\b", r"(?<!\w)компромисс\w*",
    r"(?<!\w)нескольк\w*\s+(?:област|домен|критери|вариант)\w*",
    r"(?<!\w)архитектур\w*\s+решен\w*",
)

DECISION_CRITERIA = (
    r"\bcosts?\b", r"\bprice\b", r"\bbudget\b", r"\bsecurity\b", r"\bprivacy\b",
    r"\boperations?\b", r"\bops\b", r"\bperformance\b", r"\breliability\b",
    r"\bmaintainability\b", r"\bscalability\b", r"\buser experience\b", r"\bux\b",
    r"\btimeline\b", r"\bschedule\b", r"\brisk\w*\b", r"\blegal\b", r"\bcompliance\b",
    r"(?<!\w)стоимост\w*", r"(?<!\w)цен\w*", r"(?<!\w)бюджет\w*",
    r"(?<!\w)безопасност\w*", r"(?<!\w)приватност\w*", r"(?<!\w)эксплуатац\w*",
    r"(?<!\w)производительност\w*", r"(?<!\w)надежност\w*", r"(?<!\w)масштабируемост\w*",
    r"(?<!\w)срок\w*", r"(?<!\w)риск\w*", r"(?<!\w)закон\w*", r"(?<!\w)соответств\w*",
)

DECISION_INTENT = (
    r"\bshould\s+i\b", r"\bshould\s+we\b", r"\bwould\s+you\s+recommend\b",
    r"\brecommend\w*\b", r"\bdecide\w*\b", r"\bchoose\w*\b", r"\bwhich\s+(?:option|one)\b",
    r"\bis\s+it\s+worth\b", r"\bwhether\s+to\b",
    r"(?<!\w)стоит\s+ли\b", r"(?<!\w)посовет\w*", r"(?<!\w)рекоменду\w*",
    r"(?<!\w)выбрат\w*", r"(?<!\w)решит\w*", r"(?<!\w)какой\s+вариант\b",
)

README_STANDARD = (
    r"\bfull\s+redesign\b", r"\bwhole\s+readme\b", r"\brebrand\w*\b",
    r"(?<!\w)полный\w*\s+редизайн", r"(?<!\w)полност\w*\s+переработ\w*", r"(?<!\w)переработ\w*\s+readme",
)

PROJECT_ASSESSMENT = (
    r"\b(?:review|assess|evaluate|audit|critique|analy[sz]e)\b.{0,100}\b(?:project|codebase|repository|source\s+code)\b",
    r"\b(?:project|codebase|repository|source\s+code)\b.{0,60}\b(?:review|assessment|audit|evaluation)\b",
    r"(?<!\w)(?:оцени|оцените|проверь|проверить|проанализируй|проанализировать|проведи\s+аудит|сделай\s+ревью)\w*.{0,100}(?:проект\w*|код\w*|репозитор\w*)",
    r"(?<!\w)(?:оценк|ревью|аудит|анализ)\w*.{0,60}(?:проект\w*|код\w*|репозитор\w*)",
)

PROJECT_PERSPECTIVES = (
    r"\b(?:multiple|different|several)\s+(?:perspectives|angles|viewpoints|dimensions)\b",
    r"\b(?:holistic|cross[- ]functional)\s+(?:review|assessment|evaluation)\b",
    r"\bcomprehensive\s+(?:project|codebase|repository|source\s+code)\s+(?:review|assessment|evaluation)\b",
    r"(?<!\w)(?:с\s+разн\w*\s+сторон|с\s+нескольк\w*\s+точек\s+зрения|по\s+нескольк\w*\s+аспект\w*|всесторонн\w*\s+(?:оценк|ревью|анализ)\w*|комплексн\w*\s+(?:оценк|ревью|анализ)\w*)",
)

PROJECT_REVIEW_CRITERIA = (
    r"\barchitectur\w*\b", r"\bmaintainab\w*\b", r"\bperformance\b",
    r"\bsecurity\b", r"\b(?:usability|user experience|ux)\b", r"\b(?:test coverage|testing)\b",
    r"\bcode quality\b", r"\bscalab\w*\b", r"\bdeploy\w*\b", r"\bmaintenan\w*\b",
    r"(?<!\w)архитектур\w*", r"(?<!\w)поддерживаемост\w*", r"(?<!\w)производительност\w*",
    r"(?<!\w)безопасност\w*", r"(?<!\w)удобств\w*\s+использован\w*",
    r"(?<!\w)тестирован\w*", r"(?<!\w)качеств\w*\s+код\w*", r"(?<!\w)масштабируемост\w*",
)

BEGINNER_IDEA = (
    r"\b(?:idea|concept)\b.{0,60}\b(?:app|application|product|project|service|startup|website)\b", r"\b(?:app|application|product|project|service|startup|website)\b.{0,60}\b(?:to|for)\b.{0,60}\b(?:track|schedule|book|manage)\b",
    r"\b(?:app|application|product|project|service|startup|website)\b.{0,60}\b(?:idea|concept)\b",
    r"(?<!\w)иде[яию]\b.{0,60}(?:приложен\w*|продукт\w*|проект\w*|сервис\w*|сайт\w*|стартап\w*)",
    r"(?<!\w)(?:приложен\w*|продукт\w*|проект\w*|сервис\w*|сайт\w*|стартап\w*).{0,60}иде[яию]\b", r"(?<!\w)иде[яию]\b.{0,60}(?:сделать|создать|разработать)\s+(?:приложен\w*|продукт\w*|проект\w*|сервис\w*|сайт\w*|стартап\w*)",
)

BEGINNER_CONTEXT = (
    r"\b(?:beginner|newbie|novice|new to coding|no coding experience|vague idea|rough idea|don't know where to start|not sure where to start)\b", r"\b(?:i'm|i am)\s+(?:a\s+)?beginner\b",
    r"(?<!\w)(?:нович\w*|начинающ\w*|без\s+опыта|смутн\w*\s+иде[яию]|не\s+знаю,?\s+с\s+чего\s+начать|есть\s+иде[яию]\b)",
)

BEGINNER_INTENT = (
    r"\b(?:where|how)\s+(?:do|should|can)\s+i\s+(?:start|begin)\b",
    r"\b(?:help|guide|walk)\s+me\b", r"\b(?:first steps?|get started)\b",
    r"(?<!\w)(?:с\s+чего\s+начать|помоги\w*|подскажи\w*|проведи\w*\s+по\s+шагам|первые\s+шаги|перв\w*\s+шаг\w*)",
)


INFORMATIONAL_QUERY = (
    r"^\s*(?:what\s+(?:is|are)|explain|define|describe|how\s+does)\b",
    r"^\s*(?:что\s+такое|кто\s+такой|объясни|опиши|как\s+работает)\b",
)

INFORMATIONAL_ACTION = (
    r"\b(?:create|write|improve|rewrite|redesign|update|humanize|naturalize|use|apply|run|invoke|compare|choose|recommend)\b",
    r"\b(?:audit|review|scan)\s+(?:this|the|my|our)\b",
    r"(?<!\w)(?:созд|напиш|улучш|перепиш|обнов|оформ|гуманиз|сравн|выбер|посовет|использ|примен|запуст)\w*",
    r"(?<!\w)проверь\w*\s+(?:этот|данн|мой|наш)\w*",
)

WEATHER_LOOKUP = (
    r"\bweather\s+forecast\b",
    r"\bforecast\s+(?:for|in)\s+.{1,80}\b(?:today|tomorrow|tonight|weekend)\b",
    r"(?<!\w)прогноз\w*\s+погод\w*",
    r"(?<!\w)прогноз\w*.{1,80}(?:сегодня|завтра|на\s+выходн)\w*",
)

SPECIALIST_PRIORITY = ("SECURITY_REVIEW", "README_STUDIO", "PROMPT_ENGINEER", "UPSTREAM_MAINTENANCE", "HUMANIZE")
EXTERNAL_SKILL_BY_ROUTE = {"HUMANIZE": "humanizer", "README_STUDIO": "beautify-github-readme"}
ANALYTIC_OVERLAYS = {"AUDIT", "VERIFY", "PLAN", "IDEATE", "FORECAST", "MEDIATE", "RESEARCH", "HARNESS", "SECURITY", "CRITIQUE", "DECISION", "PRE_MORTEM", "LEARN"}
MODE_ACTIONS = {
    "IDEATE": (r"\bbrainstorm\w*\b", r"\b(?:generate|come\s+up\s+with)\s+(?:some\s+)?(?:ideas|options)\b", r"(?<!\w)(?:провед\w*\s+мозгов\w*\s+штурм|мозгов\w*\s+штурм)"),
    "CRITIQUE": (r"\b(?:critique|criticize|challenge|stress[- ]test)\b", r"(?<!\w)(?:раскритикуй|покритикуй|оспорь)"),
    "DECISION": (r"\bhelp\s+me\s+(?:decide|choose)\b", r"\bchoose\s+which\b", r"(?<!\w)помоги\w*\s+выбрат\w*"),
    "PRE_MORTEM": (r"\b(?:what\s+could\s+go\s+wrong|assume\s+(?:the\s+)?(?:plan|launch|project)\s+failed)\b", r"(?<!\w)(?:сделай\w*\s+премортем|что\s+может\s+пойти\s+не\s+так)"),
    "LEARN": (r"\b(?:teach\s+me|help\s+me\s+learn)\b", r"(?<!\w)(?:научи\w*|обучи\w*|объясни\s+мне)"),
}


def requested_modes(text: str) -> list[str]:
    return [name for name, patterns in MODE_ACTIONS.items() if matches(text, patterns)]


def matches(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE | re.UNICODE) for pattern in patterns)


def count_matches(text: str, patterns: tuple[str, ...]) -> int:
    return sum(bool(re.search(pattern, text, re.IGNORECASE | re.UNICODE)) for pattern in patterns)


def choose_specialist(overlays: list[str]) -> str | None:
    for name in SPECIALIST_PRIORITY:
        if name in overlays:
            return name
    return None


def route(request: str) -> dict[str, object]:
    text = request.casefold()
    requested = requested_modes(text)
    overlays = [rule.name for rule in RULES if rule.name not in {"IDEATE", "CRITIQUE", "DECISION", "PRE_MORTEM", "LEARN"} and matches(text, rule.patterns)]
    explicit = matches(text, EXPLICIT_PANEL)
    mode_requested = bool(requested)
    overlays.extend(name for name in requested if name not in overlays)
    specialist = choose_specialist(overlays)
    informational_only = matches(text, INFORMATIONAL_QUERY) and not matches(text, INFORMATIONAL_ACTION) and not mode_requested
    weather_lookup = matches(text, WEATHER_LOOKUP)
    project_criteria = count_matches(text, PROJECT_REVIEW_CRITERIA)
    non_security_criterion = matches(text, tuple(
        pattern for pattern in PROJECT_REVIEW_CRITERIA
        if "security" not in pattern and "безопасност" not in pattern
    ))
    project_review = bool(
        not informational_only
        and matches(text, PROJECT_ASSESSMENT)
        and (matches(text, PROJECT_PERSPECTIVES) or (non_security_criterion and project_criteria >= 2))
        and (specialist is None or (specialist == "SECURITY_REVIEW" and non_security_criterion))
    )
    beginner_guide = bool(
        not informational_only
        and not project_review
        and not mode_requested
        and specialist is None
        and matches(text, BEGINNER_IDEA)
        and matches(text, BEGINNER_CONTEXT)
        and matches(text, BEGINNER_INTENT)
    )
    if informational_only and not explicit:
        specialist = None
    if project_review:
        overlays.append("PROJECT_REVIEW")
        if specialist == "SECURITY_REVIEW":
            specialist = None
    elif beginner_guide:
        overlays.append("BEGINNER_GUIDE")
        specialist = "BEGINNER_GUIDE"
    high_count = count_matches(text, HIGH_RISK)
    deep_count = count_matches(text, DEEP_MARKERS)
    comparison_count = count_matches(text, COMPARISON_MARKERS)
    tradeoff_count = count_matches(text, TRADEOFF_MARKERS)
    criterion_count = count_matches(text, DECISION_CRITERIA)
    decision_intent = matches(text, DECISION_INTENT)
    analytic = [name for name in overlays if name in ANALYTIC_OVERLAYS]

    # A generic comparison is not automatically multi-domain. Require at least two
    # material criteria, or explicit architecture/trade-off language plus a criterion.
    multi_domain = bool(
        (comparison_count and criterion_count >= 2)
        or (tradeoff_count and criterion_count >= 1)
        or matches(text, (r"\bmultiple\s+domains?\b", r"\bcross[- ]functional\b", r"(?<!\w)нескольк\w*\s+(?:област|домен|критери)\w*"))
    )
    high_stakes_decision = bool(high_count and decision_intent)

    reasons: list[str] = []
    if explicit:
        reasons.append("explicit expert-panel request")
    if specialist:
        reasons.append(f"specialist route: {specialist}")
    if project_review:
        reasons.append("multi-perspective project review")
    if high_count:
        reasons.append(f"high-risk signals: {high_count}")
    if high_stakes_decision:
        reasons.append("high-stakes decision intent")
    if comparison_count and not multi_domain:
        reasons.append("generic comparison without multiple material criteria")
    if multi_domain:
        reasons.append(f"multi-domain decision: {criterion_count} material criteria")
    if len(analytic) >= 2:
        reasons.append(f"multiple analytic overlays: {', '.join(analytic)}")

    formal_single = any(name in overlays for name in ("AUDIT", "FORECAST", "MEDIATE", "RESEARCH"))
    if informational_only or (weather_lookup and "FORECAST" in overlays):
        formal_single = False
    cross_domain = len(set(analytic)) >= 2 or multi_domain
    trigger = bool(
        explicit
        or specialist
        or project_review
        or (len(analytic) >= 2 and not informational_only)

        or formal_single
        or high_stakes_decision
        or multi_domain
        or mode_requested
    )

    if not trigger:
        depth = "DIRECT"
    elif deep_count or (high_count >= 2 and (formal_single or specialist == "SECURITY_REVIEW")):
        depth = "DEEP"
    elif explicit or project_review or cross_domain or formal_single or high_stakes_decision or "PRE_MORTEM" in overlays:
        depth = "STANDARD"
    else:
        depth = "QUICK"

    # Specialist payload size must not manufacture complexity. Escalate only on task signals.
    if mode_requested and not explicit and len(requested) == 1 and not high_stakes_decision:
        depth = "STANDARD" if requested[0] == "PRE_MORTEM" else "QUICK"
    elif specialist == "HUMANIZE" and not explicit:
        other_material = set(overlays) - {"HUMANIZE", "VERIFY"}
        depth = "STANDARD" if other_material or high_stakes_decision else "QUICK"
    elif specialist == "README_STUDIO" and not explicit:
        if matches(text, README_STANDARD) or len(set(overlays) - {"README_STUDIO", "VERIFY"}) >= 2:
            depth = "STANDARD"
        elif depth == "DEEP" and not high_count:
            depth = "STANDARD"
        else:
            depth = "QUICK" if depth == "DIRECT" else depth
    elif specialist == "PROMPT_ENGINEER" and not explicit:
        depth = "STANDARD" if "HARNESS" in overlays or high_stakes_decision or multi_domain else "QUICK"
    elif specialist == "UPSTREAM_MAINTENANCE" and not explicit:
        depth = "STANDARD" if "AUDIT" in overlays or "SECURITY" in overlays or multi_domain else "QUICK"
    elif specialist == "SECURITY_REVIEW" and not explicit:
        depth = "DEEP" if deep_count or high_count >= 2 else "STANDARD"
    elif specialist == "BEGINNER_GUIDE" and not explicit:
        depth = "QUICK"

    inherent = {
        "SECURITY_REVIEW": {"SECURITY", "AUDIT"},
        "README_STUDIO": set(),
        "PROMPT_ENGINEER": set(),
        "UPSTREAM_MAINTENANCE": {"VERIFY"},
        "HUMANIZE": set(),
        "BEGINNER_GUIDE": {"IDEATE"},
    }.get(specialist, set())
    material_extras = set(overlays) - ({specialist, "VERIFY"} | inherent) if specialist else set()

    if depth == "DIRECT":
        execution = "direct"
        panel = "0"
    elif mode_requested and not explicit and len(requested) == 1 and not high_stakes_decision:
        execution = "specialist"
        panel = {"QUICK": "1–2 specialist roles", "STANDARD": "2–4 specialist roles", "DEEP": "3–5 specialist roles"}[depth]
    elif explicit or (specialist and len(material_extras) >= 2):
        execution = "panel"
        panel = {"QUICK": "3–4", "STANDARD": "5–7", "DEEP": "7–10"}[depth]
    elif specialist:
        execution = "specialist"
        panel = {"QUICK": "1–2 specialist roles", "STANDARD": "2–4 specialist roles", "DEEP": "3–5 specialist roles"}[depth]
    else:
        execution = "panel"
        panel = {"QUICK": "3–4", "STANDARD": "5–7", "DEEP": "7–10"}[depth]

    load_score = min(6, high_count * 2 + min(2, criterion_count if multi_domain else 0) + min(2, len(analytic)))
    return {
        "trigger": trigger,
        "depth": depth,
        "overlays": overlays,
        "specialist_route": specialist,
        "preferred_external_skill": EXTERNAL_SKILL_BY_ROUTE.get(specialist),
        "load_score": load_score,
        "payload_chars": len(request),
        "panel_size": panel,
        "execution": execution,
        "reasons": reasons,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Route an Expert Panel request without using payload length as a complexity proxy.")
    parser.add_argument("request")
    print(json.dumps(route(parser.parse_args().request), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
