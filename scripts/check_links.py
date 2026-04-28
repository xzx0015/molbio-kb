#!/usr/bin/env python3
"""Validate local links in generated static HTML/Markdown files."""
from __future__ import annotations

import html.parser
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
CHECK_ROOTS = [ROOT / "docs", ROOT]
SKIP_DIRS = {".git", ".github", "node_modules", "__pycache__"}
SKIP_FILES = {
    ROOT / "content/chapters/index.html",
    ROOT / "content/chapters/nav-template.html",
    ROOT / "content/chapters/template.html",
    ROOT / "content/skills/index.html",
}
SKIP_FILE_GLOBS = [
    ROOT / "content/chapters/*.html",
]


class LinkParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.links.append(value)


def iter_files() -> list[Path]:
    files: list[Path] = []
    seen: set[Path] = set()
    for base in CHECK_ROOTS:
        if not base.exists():
            continue
        for fp in base.rglob("*"):
            if any(part in SKIP_DIRS for part in fp.parts):
                continue
            if fp.resolve() in {p.resolve() for p in SKIP_FILES}:
                continue
            if any(fp.match(str(pattern)) for pattern in SKIP_FILE_GLOBS):
                continue
            if fp.suffix.lower() in {".html", ".md"} and fp.resolve() not in seen:
                files.append(fp)
                seen.add(fp.resolve())
    return sorted(files)


def extract_links(fp: Path) -> list[str]:
    text = fp.read_text(encoding="utf-8", errors="ignore")
    links: list[str] = []
    if fp.suffix.lower() == ".html":
        parser = LinkParser()
        parser.feed(text)
        links.extend(parser.links)
    # Markdown links/images. Kept intentionally simple for KB docs.
    import re

    code_spans: list[tuple[int, int]] = []
    # For HTML files, also skip <code> and <pre> blocks
    if fp.suffix.lower() == ".html":
        for match in re.finditer(r"<code[^>]*>.*?</code>", text, re.DOTALL):
            code_spans.append(match.span())
        for match in re.finditer(r"<pre[^>]*>.*?</pre>", text, re.DOTALL):
            code_spans.append(match.span())
    else:
        for match in re.finditer(r"`[^`]*`", text):
            code_spans.append(match.span())
        for match in re.finditer(r"```[\s\S]*?```", text):
            code_spans.append(match.span())

    def in_code(pos: int) -> bool:
        return any(start <= pos < end for start, end in code_spans)

    for match in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        if not in_code(match.start()):
            links.append(match.group(1))
    return links


def should_skip(link: str) -> bool:
    if not link or link.startswith("#"):
        return True
    parsed = urlparse(link)
    return bool(parsed.scheme in {"http", "https", "mailto", "tel", "javascript", "data"})


def resolve_link(src: Path, link: str) -> Path:
    parsed = urlparse(link)
    raw_path = unquote(parsed.path)
    if raw_path.startswith("/"):
        target = ROOT / raw_path.lstrip("/")
    else:
        target = src.parent / raw_path
    if target.is_dir():
        target = target / "index.html"
    return target.resolve()


def main() -> int:
    files = iter_files()
    errors: list[tuple[Path, str, Path]] = []
    checked = 0
    for fp in files:
        for link in extract_links(fp):
            # Strip title portion in Markdown links: path "title"
            link = link.strip().split()[0].strip('"\'')
            if should_skip(link):
                continue
            target = resolve_link(fp, link)
            checked += 1
            if not target.exists():
                errors.append((fp.relative_to(ROOT), link, target.relative_to(ROOT) if ROOT in target.parents else target))
    if errors:
        print(f"BROKEN LINKS: {len(errors)} / checked {checked}")
        for src, link, target in errors[:100]:
            print(f"- {src}: {link} -> {target}")
        if len(errors) > 100:
            print(f"... {len(errors)-100} more")
        return 1
    print(f"OK: checked {checked} local links across {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
