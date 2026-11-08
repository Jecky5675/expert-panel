#!/usr/bin/env python3
"""Audit README image references and baseline SVG compatibility, accessibility, and safety."""

from __future__ import annotations

import argparse
import html
import json
import re
import urllib.parse
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path

MARKDOWN_IMAGE = re.compile(r"!\[([^\]]*)\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\)")
MARKDOWN_REF_IMAGE = re.compile(r"!\[([^\]]*)\]\[([^\]]*)\]")
MARKDOWN_REF_DEF = re.compile(r"^\s*\[([^\]]+)\]:\s*(?:<([^>]+)>|([^\s]+))", re.MULTILINE)
FENCED_BLOCK = re.compile(r"(?ms)^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?^[ \t]*\1[ \t]*$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
INLINE_CODE = re.compile(r"(?<!`)`[^`\n]+`(?!`)")
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I | re.S)
CSS_FORBIDDEN = re.compile(r"@import|expression\s*\(|behavior\s*:", re.I)
SCHEME = re.compile(r"^[a-z][a-z0-9+.-]*:", re.I)
WINDOWS_ABSOLUTE = re.compile(r"^(?:[a-z]:[\\/]|\\\\)", re.I)
CONTROL_OR_SPACE = re.compile(r"[\x00-\x20\x7f]+")
UNSAFE_SVG_TAGS = {"script", "foreignobject", "iframe", "object", "embed", "applet"}
RESOURCE_TAGS = {"image", "use", "feimage", "audio", "video", "source"}
URI_ATTRS = {"href", "src", "poster"}
MAX_SVG_BYTES = 5 * 1024 * 1024
MAX_README_BYTES = 5 * 1024 * 1024
MAX_DECODE_ROUNDS = 16
SMIL_TAGS = {"animate", "animatemotion", "animatetransform", "set"}


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str
    artifact: str | None = None


def issue(severity: str, code: str, message: str, artifact: str | None = None) -> Issue:
    return Issue(severity, code, message, artifact)


def dedupe(items: list[Issue]) -> list[Issue]:
    return list(dict.fromkeys(items))


def mask_nonrendered(text: str) -> str:
    def blank(match: re.Match[str]) -> str:
        return ''.join('\n' if char == '\n' else ' ' for char in match.group(0))
    for pattern in (FENCED_BLOCK, HTML_COMMENT, INLINE_CODE):
        text = pattern.sub(blank, text)
    return text


def decode_uri(value: str) -> str:
    decoded = value.strip()
    for _ in range(MAX_DECODE_ROUNDS):
        newer = urllib.parse.unquote(html.unescape(decoded))
        if newer == decoded:
            return decoded
        decoded = newer
    return decoded


def normalize_uri(value: str) -> str:
    return CONTROL_OR_SPACE.sub('', decode_uri(value)).casefold()


def classify_uri(value: str) -> str:
    decoded = decode_uri(value).strip()
    normalized = CONTROL_OR_SPACE.sub('', decoded).casefold()
    if not normalized:
        return 'empty'
    if normalized.startswith('#'):
        return 'fragment'
    if normalized.startswith(('javascript:', 'vbscript:')):
        return 'unsafe'
    if normalized.startswith('data:'):
        return 'data'
    if normalized.startswith(('http:', 'https:', '//')):
        return 'remote'
    if WINDOWS_ABSOLUTE.match(decoded) or decoded.startswith(('/', '\\')):
        return 'absolute'
    if SCHEME.match(normalized):
        return 'unsupported'
    return 'local'


def local_target(value: str, base: Path) -> Path | None:
    if classify_uri(value) != 'local':
        return None
    decoded = decode_uri(value)
    clean = decoded.split('#', 1)[0].split('?', 1)[0]
    return (base / clean).resolve() if clean else None


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root.resolve())
        return True
    except ValueError:
        return False


def attr_local_name(name: str) -> str:
    return name.rsplit('}', 1)[-1].casefold()


class ImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[dict[str, str | None]] = []
        self.srcsets: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        lowered = tag.casefold()
        mapping = {key.casefold(): value for key, value in attrs}
        if lowered == 'img':
            self.images.append(mapping)
        if lowered in {'img', 'source'} and mapping.get('srcset'):
            self.srcsets.append((lowered, str(mapping['srcset'])))

    handle_startendtag = handle_starttag



def parse_srcset(value: str) -> list[str]:
    decoded = decode_uri(value).strip()
    if not decoded:
        return []
    if decoded.casefold().startswith('data:'):
        return [decoded]
    candidates: list[str] = []
    for item in decoded.split(','):
        candidate = item.strip().split()[0] if item.strip() else ''
        if candidate:
            candidates.append(candidate)
    return candidates

def collect_images(text: str) -> tuple[list[tuple[str, str | None, str]], list[Issue]]:
    visible = mask_nonrendered(text)
    findings: list[Issue] = []
    records: list[tuple[str, str | None, str]] = []
    definitions: dict[str, str] = {}
    for match in MARKDOWN_REF_DEF.finditer(visible):
        definitions[match.group(1).strip().casefold()] = (match.group(2) or match.group(3) or '').strip()

    for match in MARKDOWN_IMAGE.finditer(visible):
        alt, src = match.group(1), (match.group(2) or match.group(3) or '').strip()
        records.append(('Markdown', alt, src))
        if not alt.strip():
            findings.append(issue('WARNING', 'empty-alt', f'Markdown image has empty alt text; confirm it is decorative: {src}'))
        elif len(alt.strip()) > 250:
            findings.append(issue('WARNING', 'long-alt', f'Markdown image alt text is unusually long: {src}'))

    for match in MARKDOWN_REF_IMAGE.finditer(visible):
        alt, key = match.group(1), (match.group(2) or match.group(1)).strip().casefold()
        src = definitions.get(key)
        if src is None:
            findings.append(issue('ERROR', 'missing-image-reference', f'Markdown image reference is undefined: [{key}]'))
            continue
        records.append(('Markdown reference', alt, src))
        if not alt.strip():
            findings.append(issue('WARNING', 'empty-alt', f'Markdown reference image has empty alt text: {src}'))

    parser = ImageParser()
    try:
        parser.feed(visible)
    except Exception as exc:
        findings.append(issue('WARNING', 'html-parse', f'HTML image markup could not be fully parsed: {exc}'))
    for attrs in parser.images:
        src = attrs.get('src')
        if src is None:
            findings.append(issue('ERROR', 'html-img-src', 'HTML image is missing src'))
            continue
        alt = attrs.get('alt')
        records.append(('HTML', alt, src.strip()))
        if alt is None:
            findings.append(issue('WARNING', 'missing-alt', f'HTML image missing alt attribute: {src}'))
        elif not alt.strip():
            findings.append(issue('WARNING', 'empty-alt', f'HTML image has empty alt text; confirm it is decorative: {src}'))
        elif len(alt.strip()) > 250:
            findings.append(issue('WARNING', 'long-alt', f'HTML image alt text is unusually long: {src}'))
    for tag, srcset in parser.srcsets:
        for src in parse_srcset(srcset):
            records.append((f'HTML {tag} srcset', None, src))
    return records, dedupe(findings)


def inspect_resource(value: str, artifact: Path, project_root: Path, context: str) -> list[Issue]:
    kind = classify_uri(value)
    label = str(artifact)
    if kind == 'fragment' or kind == 'empty':
        return []
    if kind == 'unsafe':
        return [issue('ERROR', 'unsafe-uri', f'{context} uses an active scripting URI: {value}', label)]
    if kind == 'data':
        return [issue('ERROR', 'data-resource', f'{context} embeds a data URI: {value[:80]}', label)]
    if kind == 'remote':
        return [issue('ERROR', 'remote-svg-resource', f'{context} loads a remote resource: {value}', label)]
    if kind == 'absolute':
        return [issue('ERROR', 'absolute-resource-path', f'{context} uses an absolute path: {value}', label)]
    if kind == 'unsupported':
        return [issue('ERROR', 'unsupported-resource-scheme', f'{context} uses an unsupported URI scheme: {value}', label)]
    target = local_target(value, artifact.parent)
    if target is None:
        return []
    if not within(target, project_root):
        return [issue('ERROR', 'svg-path-escape', f'{context} escapes project root: {value}', label)]
    if not target.is_file():
        return [issue('ERROR', 'missing-svg-resource', f'{context} points to a missing local file: {value}', label)]
    if target.suffix.casefold() in {'.png', '.jpg', '.jpeg', '.webp', '.gif'}:
        return [issue('WARNING', 'external-raster-dependency', f'{context} depends on local raster asset: {value}', label)]
    return []


def inspect_css(css: str, artifact: Path, project_root: Path) -> list[Issue]:
    findings: list[Issue] = []
    if CSS_FORBIDDEN.search(css):
        findings.append(issue('ERROR', 'unsafe-css-resource', 'CSS contains @import, expression(), or behavior', str(artifact)))
    for match in CSS_URL.finditer(css):
        findings.extend(inspect_resource(match.group(2).strip(), artifact, project_root, 'CSS url()'))
    return findings


def audit_svg(path: Path, project_root: Path) -> list[Issue]:
    artifact = str(path)
    try:
        size = path.stat().st_size
    except OSError as exc:
        return [issue('ERROR', 'svg-stat', f'cannot inspect SVG: {exc}', artifact)]
    if size > MAX_SVG_BYTES:
        return [issue('ERROR', 'svg-too-large', f'SVG exceeds {MAX_SVG_BYTES // (1024*1024)} MiB preflight limit', artifact)]
    try:
        raw = path.read_text(encoding='utf-8')
    except UnicodeDecodeError as exc:
        return [issue('ERROR', 'svg-encoding', f'SVG is not valid UTF-8: {exc}', artifact)]

    findings: list[Issue] = []
    normalized_raw = normalize_uri(raw)
    if '<!doctype' in raw.casefold() or '<!entity' in raw.casefold():
        findings.append(issue('ERROR', 'svg-doctype-entity', 'DOCTYPE/ENTITY declarations are forbidden; XML parsing was skipped', artifact))
        if 'javascript:' in normalized_raw or 'vbscript:' in normalized_raw:
            findings.append(issue('ERROR', 'unsafe-uri', 'SVG contains an encoded active scripting URI', artifact))
        return dedupe(findings)
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return [issue('ERROR', 'svg-xml', f'invalid SVG XML: {exc}', artifact)]
    if attr_local_name(root.tag) != 'svg':
        findings.append(issue('ERROR', 'svg-root', 'root element is not <svg>', artifact))
    if not root.attrib.get('viewBox'):
        findings.append(issue('WARNING', 'svg-viewbox', 'SVG has no viewBox and may not scale reliably', artifact))

    ids: set[str] = set()
    has_title = False
    has_desc = False
    for element in root.iter():
        tag = attr_local_name(element.tag)
        has_title |= tag == 'title' and bool((element.text or '').strip())
        has_desc |= tag == 'desc' and bool((element.text or '').strip())
        element_id = element.attrib.get('id')
        if element_id:
            if element_id in ids:
                findings.append(issue('WARNING', 'duplicate-svg-id', f'duplicate SVG id: {element_id}', artifact))
            ids.add(element_id)
        if tag in UNSAFE_SVG_TAGS:
            findings.append(issue('ERROR', 'active-svg-tag', f'active or unsupported SVG tag: <{tag}>', artifact))
        if tag in SMIL_TAGS:
            findings.append(issue('WARNING', 'svg-animation', f'SMIL animation may be stripped or ignored by GitHub: <{tag}>', artifact))
        if tag == 'style':
            findings.extend(inspect_css(element.text or '', path, project_root))
        for raw_name, value in element.attrib.items():
            name = attr_local_name(raw_name)
            if name.startswith('on'):
                findings.append(issue('ERROR', 'svg-event-handler', f'event handler attribute is forbidden: {name}', artifact))
            if name == 'style':
                findings.extend(inspect_css(value, path, project_root))
            if name in URI_ATTRS or (tag in RESOURCE_TAGS and name.endswith('href')):
                findings.extend(inspect_resource(value, path, project_root, f'<{tag}> {name}'))
    if not has_title:
        findings.append(issue('WARNING', 'svg-title', 'SVG has no non-empty <title>', artifact))
    if not has_desc:
        findings.append(issue('WARNING', 'svg-desc', 'SVG has no non-empty <desc>', artifact))
    return dedupe(findings)


def audit_readme(readme: Path, project_root: Path) -> list[Issue]:
    try:
        size = readme.stat().st_size
    except OSError as exc:
        return [issue('ERROR', 'readme-stat', f'cannot inspect README: {exc}', str(readme))]
    if size > MAX_README_BYTES:
        return [issue('ERROR', 'readme-too-large', f'README exceeds {MAX_README_BYTES // (1024*1024)} MiB preflight limit', str(readme))]
    try:
        text = readme.read_text(encoding='utf-8')
    except UnicodeDecodeError as exc:
        return [issue('ERROR', 'readme-encoding', f'README is not valid UTF-8: {exc}', str(readme))]
    records, findings = collect_images(text)
    counts: dict[str, int] = {}
    for _kind, _alt, src in records:
        counts[src] = counts.get(src, 0) + 1
    for src, count in counts.items():
        if count > 1:
            findings.append(issue('WARNING', 'duplicate-image', f'image is referenced {count} times: {src}'))

    for src in counts:
        kind = classify_uri(src)
        if kind == 'remote':
            findings.append(issue('WARNING', 'remote-image', f'remote image cannot be verified locally: {src}'))
            continue
        if kind == 'data':
            findings.append(issue('ERROR', 'data-image', f'README embeds a data URI image: {src[:80]}'))
            continue
        if kind == 'unsafe':
            findings.append(issue('ERROR', 'unsafe-image-uri', f'README image uses an active scripting URI: {src}'))
            continue
        if kind == 'unsupported':
            findings.append(issue('ERROR', 'unsupported-image-scheme', f'README image uses an unsupported URI scheme: {src}'))
            continue
        if kind == 'absolute':
            findings.append(issue('ERROR', 'absolute-image-path', f'README image uses an absolute path: {src}'))
            continue
        if kind in {'empty', 'fragment'}:
            continue
        target = local_target(src, readme.parent)
        if target is None:
            continue
        if not within(target, project_root):
            findings.append(issue('ERROR', 'readme-path-escape', f'image path escapes project root: {src}'))
            continue
        if not target.is_file():
            findings.append(issue('ERROR', 'missing-image', f'missing image: {src}'))
            continue
        if target.suffix.casefold() == '.svg':
            findings.extend(audit_svg(target, project_root))
    return dedupe(findings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('readme', help='Path to README.md')
    parser.add_argument('--root', help='Project root; defaults to the README directory')
    parser.add_argument('--json', action='store_true', dest='as_json', help='Emit machine-readable JSON')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as failures')
    args = parser.parse_args()
    readme = Path(args.readme).expanduser().resolve()
    if not readme.is_file():
        print(f'ERROR: README not found: {readme}')
        return 2
    project_root = Path(args.root).expanduser().resolve() if args.root else readme.parent
    if not project_root.is_dir() or not within(readme, project_root):
        print(f'ERROR: invalid project root for README: {project_root}')
        return 2
    findings = audit_readme(readme, project_root)
    errors = [item for item in findings if item.severity == 'ERROR']
    warnings = [item for item in findings if item.severity == 'WARNING']
    payload = {'readme': str(readme), 'project_root': str(project_root), 'errors': len(errors), 'warnings': len(warnings), 'issues': [asdict(item) for item in findings]}
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f'README: {readme}')
        print(f'Project root: {project_root}')
        print(f'Errors: {len(errors)} | Warnings: {len(warnings)}')
        for item in findings:
            location = f' [{item.artifact}]' if item.artifact else ''
            print(f'- {item.severity} {item.code}{location}: {item.message}')
        if not findings:
            print('OK: image references, paths, alt text, and SVG baseline checks passed')
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == '__main__':
    raise SystemExit(main())
