#!/usr/bin/env python3
"""Собирает статический HTML-сайт из markdown-файлов базы знаний."""

from __future__ import annotations

import re
import shutil
from pathlib import Path, PurePosixPath

import markdown

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
STATIC = ROOT / "static"

MARKDOWN_SOURCES = [
    (ROOT / "README.md", DIST / "index.html"),
    (ROOT / "general" / "overview.md", DIST / "general-overview.html"),
    *(
        (path, DIST / f"roles-{path.stem}.html")
        for path in sorted((ROOT / "roles").glob("*.md"))
    ),
]

LINK_PATTERN = re.compile(r"(\[[^\]]*\]\()([^)#]+)\.md([^)]*\))")


def to_flat_html(md_path: str) -> str:
    path, anchor = (md_path.split("#", 1) + [""])[:2]
    anchor = f"#{anchor}" if anchor else ""

    normalized = PurePosixPath(path.strip().lstrip("./"))
    while normalized.parts and normalized.parts[0] == "..":
        normalized = PurePosixPath(*normalized.parts[1:])

    if normalized.name in {"README.md", "readme.md"}:
        return f"index.html{anchor}"

    stem = normalized.stem
    if normalized.parts and normalized.parts[0] == "general":
        return f"general-{stem}.html{anchor}"

    return f"roles-{stem}.html{anchor}"


def rewrite_links(text: str) -> str:
    return LINK_PATTERN.sub(
        lambda match: f"{match.group(1)}{to_flat_html(match.group(2))}{match.group(3)}",
        text,
    )


def page_title(source: Path, body_html: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", body_html, re.DOTALL)
    if match:
        return re.sub(r"<[^>]+>", "", match.group(1)).strip()
    return source.stem.replace("_", " ").title()


def render_page(source: Path, output: Path, body_html: str) -> None:
    title = page_title(source, body_html)
    output.write_text(
        f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — С95</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="index.html">С95 · База знаний волонтёров</a>
    </div>
  </header>
  <main class="container content">
    {body_html}
  </main>
  <footer class="site-footer">
    <div class="container">
      <p>База знаний сообщества С95</p>
    </div>
  </footer>
</body>
</html>
""",
        encoding="utf-8",
    )


def build() -> None:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists"])

    for source, output in MARKDOWN_SOURCES:
        text = rewrite_links(source.read_text(encoding="utf-8"))
        body_html = md.convert(text)
        md.reset()
        render_page(source, output, body_html)

    shutil.copy2(STATIC / "style.css", DIST / "style.css")
    print(f"Built {len(MARKDOWN_SOURCES)} pages into {DIST}")


if __name__ == "__main__":
    build()
