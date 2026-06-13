#!/usr/bin/env python3
"""Публикует содержимое dist/ в GitHub Gist."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DIST = Path(__file__).resolve().parent.parent / "dist"
BATCH_SIZE = 10


def gist_request(
    gist_id: str,
    gist_token: str,
    payload: dict,
) -> dict:
    request = urllib.request.Request(
        f"https://api.github.com/gists/{gist_id}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {gist_token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "s95-kb-publish",
        },
        method="PATCH",
    )

    with urllib.request.urlopen(request) as response:
        return json.load(response)


def validate_filename(name: str) -> None:
    if "/" in name or "\\" in name or name in {".", ".."}:
        raise ValueError(f"Недопустимое имя файла для Gist: {name}")


def main() -> None:
    gist_id = os.environ.get("GIST_ID", "").strip()
    gist_token = os.environ.get("GIST_TOKEN", "").strip()

    if not gist_id or not gist_token:
        print(
            "GIST_ID и GIST_TOKEN должны быть заданы в secrets репозитория.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not DIST.is_dir():
        print(f"Каталог {DIST} не найден. Сначала запустите build_static.py.", file=sys.stderr)
        sys.exit(1)

    files: dict[str, dict[str, str]] = {}
    for path in sorted(DIST.rglob("*")):
        if path.is_file():
            rel = path.relative_to(DIST).as_posix()
            validate_filename(rel)
            files[rel] = {"content": path.read_text(encoding="utf-8")}

    file_items = list(files.items())
    data: dict | None = None

    for start in range(0, len(file_items), BATCH_SIZE):
        batch = dict(file_items[start : start + BATCH_SIZE])
        payload = {
            "description": "С95 — статическая база знаний волонтёров",
            "files": batch,
        }
        try:
            data = gist_request(gist_id, gist_token, payload)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            names = ", ".join(batch)
            print(
                f"Ошибка публикации в Gist ({exc.code}) для файлов: {names}\n{body}",
                file=sys.stderr,
            )
            sys.exit(1)

    if data is None:
        print("Нет файлов для публикации.", file=sys.stderr)
        sys.exit(1)

    owner = data["owner"]["login"]
    gist_url = data["html_url"]
    preview_url = (
        "https://htmlpreview.github.io/?"
        f"https://gist.githubusercontent.com/{owner}/{gist_id}/raw/index.html"
    )

    print(f"Gist обновлён: {gist_url}")
    print(f"Просмотр сайта: {preview_url}")
    print(f"Файлов опубликовано: {len(files)}")


if __name__ == "__main__":
    main()
