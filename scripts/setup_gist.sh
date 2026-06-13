#!/usr/bin/env bash
# Одноразовая настройка публикации базы знаний в GitHub Gist.
#
# Использование:
#   export GITHUB_TOKEN=ghp_...   # PAT с правом gist
#   ./scripts/setup_gist.sh
#
# Или с уже существующим gist:
#   export GITHUB_TOKEN=ghp_...
#   export GIST_ID=abc123...
#   ./scripts/setup_gist.sh

set -euo pipefail

REPO="${REPO:-vutratenko/s95-kb}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

show_manual_secrets() {
  cat <<EOF

Добавьте secrets вручную:
  Репозиторий → Settings → Secrets and variables → Actions

  GIST_TOKEN = <ваш PAT с правом gist>
  GIST_ID    = $GIST_ID

Или через gh cli:
  gh secret set GIST_TOKEN --repo $REPO
  gh secret set GIST_ID --repo $REPO
EOF
}

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  echo "Задайте GITHUB_TOKEN — Personal Access Token с правом gist." >&2
  echo "Создать: https://github.com/settings/tokens" >&2
  exit 1
fi

export GIST_TOKEN="$GITHUB_TOKEN"

cd "$ROOT"

if ! command -v python3 >/dev/null; then
  echo "Нужен python3." >&2
  exit 1
fi

pip install -q -r scripts/requirements.txt
python3 scripts/build_static.py

if [[ -z "${GIST_ID:-}" ]]; then
  echo "Создаю публичный gist..."
  response="$(curl -fsSL -X POST \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "Content-Type: application/json" \
    -d '{"description":"С95 — статическая база знаний волонтёров","public":true,"files":{"index.html":{"content":"placeholder"}}}' \
    https://api.github.com/gists)"
  GIST_ID="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])' <<<"$response")"
  owner="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["owner"]["login"])' <<<"$response")"
  echo "Gist создан: https://gist.github.com/$owner/$GIST_ID"
else
  owner="$(curl -fsSL \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/gists/$GIST_ID" | python3 -c 'import json,sys; print(json.load(sys.stdin)["owner"]["login"])')"
  echo "Использую существующий gist: https://gist.github.com/$owner/$GIST_ID"
fi

export GIST_ID
python3 scripts/publish_gist.py

preview_url="https://htmlpreview.github.io/?https://gist.githubusercontent.com/$owner/$GIST_ID/raw/index.html"
echo ""
echo "Сайт: $preview_url"
echo ""

if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then
  echo "Добавляю secrets в репозиторий $REPO..."
  if printf '%s' "$GITHUB_TOKEN" | gh secret set GIST_TOKEN --repo "$REPO"; then
    printf '%s' "$GIST_ID" | gh secret set GIST_ID --repo "$REPO"
    echo "Secrets GIST_TOKEN и GIST_ID добавлены."
    echo "При следующем push в main сайт обновится автоматически."
  else
    show_manual_secrets
  fi
else
  show_manual_secrets
fi
