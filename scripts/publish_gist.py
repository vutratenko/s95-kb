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
API = "https://api.github.com"


def api_request(
    method: str,
    path: str,
    gist_token: str,
    payload: dict | None = None,
) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{API}{path}",
        data=data,
        headers={
            "Authorization": f"Bearer {gist_token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "s95-kb-publish",
        },
        method=method,
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def validate_filename(name: str) -> None:
    if "/" in name or "\\" in name or name in {".", ".."}:
        raise ValueError(f"Недопустимое имя файла для Gist: {name}")


def collect_dist_files() -> dict[str, dict[str, str]]:
    files: dict[str, dict[str, str]] = {}
    for path in sorted(DIST.rglob("*")):
        if path.is_file():
            rel = path.relative_to(DIST).as_posix()
            validate_filename(rel)
            files[rel] = {"content": path.read_text(encoding="utf-8")}
    return files


def stale_gist_files(existing: dict) -> dict[str, None]:
    stale: dict[str, None] = {}
    for name in existing:
        if "/" in name or "\\" in name:
            stale[name] = None
    return stale


def main() -> None:
    gist_id = os.environ.get("GIST_ID", "").strip()
    gist_token = os.environ.get("GIST_TOKEN", "").strip()

    if not gist_id or not gist_token:
        print("Пропуск публикации: GIST_TOKEN или GIST_ID не заданы в secrets.")
        return

    if not DIST.is_dir():
        print(f"Каталог {DIST} не найден. Сначала запустите build_static.py.", file=sys.stderr)
        sys.exit(1)

    files = collect_dist_files()
    if not files:
        print("Нет файлов для публикации.", file=sys.stderr)
        sys.exit(1)

    try:
        current = api_request("GET", f"/gists/{gist_id}", gist_token)
        payload_files = {**stale_gist_files(current.get("files", {})), **files}
        data = api_request(
            "PATCH",
            f"/gists/{gist_id}",
            gist_token,
            {
                "description": "С95 — статическая база знаний волонтёров",
                "files": payload_files,
            },
        )
    except RuntimeError as exc:
        print(f"Ошибка публикации в Gist: {exc}", file=sys.stderr)
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
