#!/usr/bin/env python3
"""Audit the publishable three-folder repository, not generated archives."""
from __future__ import annotations
import argparse,re,sys
from pathlib import Path
MAX_FILE_BYTES=8*1024*1024
ALLOWED_ROOT_FILES={"README.md","README_RU.md","LICENSE",".gitignore",".gitattributes"}
ALLOWED_ROOT_DIRS={"skills","docs","scripts"}
SKIP={".git","__pycache__","node_modules",".venv","venv","dist","build"}
FORBIDDEN_NAMES={".env",".npmrc",".pypirc",".netrc","credentials.json","service-account.json","id_rsa","id_ed25519"}
FORBIDDEN_SUFFIXES={".pem",".key",".p12",".pfx",".jks",".keystore",".log",".trace",".sqlite",".sqlite3",".db",".bak",".orig",".zip",".tgz",".whl"}
TOKENS=(('private key',re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC |DSA |PGP )?PRIVATE KEY-----')),('GitHub token',re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b')),('AWS access key',re.compile(r'\bAKIA[0-9A-Z]{16}\b')),('Google API key',re.compile(r'\bAIza[0-9A-Za-z_-]{35}\b')))
LOCAL=re.compile(r'\b[A-Za-z]:\\Users\\[^\s`"\']+')

def allowed(rel:Path)->bool:
    if len(rel.parts)==1:return rel.name in ALLOWED_ROOT_FILES
    if rel.parts[0] not in ALLOWED_ROOT_DIRS:return False
    suffix=rel.suffix.lower()
    if rel.parts[0]=="skills":return suffix in {".md",".json",".yaml",".yml",".txt",".csv",".svg",".gif",".png"}
    if rel.parts[0]=="docs":return suffix in {".md",".txt",".json",".yaml",".yml"}
    return suffix in {".py",".mjs",".js",".json",".toml",".txt",".md",".yml",".yaml"}

def audit(root:Path)->list[str]:
    errors=[]
    for p in sorted(root.rglob('*')):
        rel=p.relative_to(root)
        if set(rel.parts)&SKIP:continue
        if p.is_symlink():errors.append(f"symlink forbidden: {rel}");continue
        if p.is_dir():continue
        if not allowed(rel):errors.append(f"file outside skills/docs/scripts allowlist: {rel}")
        if p.name.casefold() in FORBIDDEN_NAMES or p.suffix.casefold() in FORBIDDEN_SUFFIXES:errors.append(f"sensitive/generated file forbidden: {rel}")
        try:
            if p.stat().st_size>MAX_FILE_BYTES:errors.append(f"file too large: {rel}");continue
            if p.suffix.casefold() not in {".md",".txt",".py",".mjs",".js",".json",".toml",".yaml",".yml",".csv",".svg"}:continue
            text=p.read_text(encoding="utf-8")
        except (OSError,UnicodeError) as e:errors.append(f"unreadable file {rel}: {e}");continue
        if rel.as_posix()!="scripts/audit_release.py":
            for label,pattern in TOKENS:
                if pattern.search(text):errors.append(f"possible {label} in {rel}")
            if LOCAL.search(text):errors.append(f"local absolute user path in {rel}")
    return sorted(set(errors))

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("root",nargs="?",default=".");root=Path(ap.parse_args().root).resolve()
    if not (root/"skills/expert-panel/SKILL.md").is_file():raise SystemExit(f"not the three-directory Expert Panel repository: {root}")
    errors=audit(root)
    for e in errors:print("ERROR:",e)
    print(f"Release tree audit: {len(errors)} issue(s)")
    raise SystemExit(1 if errors else 0)
if __name__=="__main__":main()
