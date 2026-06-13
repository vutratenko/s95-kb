#!/usr/bin/env python3
"""Собирает статический HTML-сайт из markdown-файлов базы знаний."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
STATIC = ROOT / "static"

MARKDOWN_SOURCES = [
    (ROOT / "README.md", DIST / "index.html"),
    (ROOT / "general" / "overview.md", DIST / "general" / "overview.html"),
    *(
        (path, DIST / "roles" / f"{path.stem}.html")
        for path in sorted((ROOT / "roles").glob("*.md"))
    ),
]

LINK_PATTERN = re.compile(r"(\[[^\]]*\]\([^)#]+)\.md([^)]*\))")


def rewrite_links(text: str) -> str:
    return LINK_PATTERN.sub(r"\1.html\2", text)


def css_href(output_path: Path) -> str:
    depth = len(output_path.relative_to(DIST).parts) - 1
    return f"{'../' * depth}style.css"


def home_href(output_path: Path) -> str:
    depth = len(output_path.relative_to(DIST).parts) - 1
    return f"{'../' * depth}index.html"


def page_title(source: Path, body_html: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", body_html, re.DOTALL)
    if match:
        return re.sub(r"<[^>]+>", "", match.group(1)).strip()
    return source.stem.replace("_", " ").title()


def render_page(source: Path, output: Path, body_html: str) -> None:
    title = page_title(source, body_html)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — С95</title>
  <link rel="stylesheet" href="{css_href(output)}">
</head>
<body>
  <header class="site-header">
    <div class="container">
      <a class="brand" href="{home_href(output)}">С95 · База знаний волонтёров</a>
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
