# Как устроен проект и как его править

Эта база знаний — обычные текстовые файлы в формате Markdown. Из них автоматически собирается сайт на GitHub Pages. Стартовая страница сайта — это файл [`README.md`](README.md), а сам сайт открывается по адресу **https://vutratenko.github.io/s95-kb/**.

Если вы пришли только почитать — вам сюда не нужно, открывайте [сайт](https://vutratenko.github.io/s95-kb/). Этот файл для тех, кто хочет поправить тексты или разобраться, как всё собирается.

## Как поправить текст

1. Найдите нужный файл: стартовая страница — `README.md`, общее описание — `general/overview.md`, а статьи про роли — в папке `roles/`.
2. Отредактируйте его прямо на GitHub (карандаш в правом верхнем углу файла) или локально.
3. Сохраните изменения в ветку `main` (через pull request). Сайт пересоберётся и обновится сам.

## Структура файлов

```
.
├── README.md                          # Стартовая страница сайта
├── CONTRIBUTING.md                    # Этот файл
├── general/
│   └── overview.md                    # Общее описание волонтёрства
├── roles/                             # Статьи про каждую роль (по одному .md на роль)
│   ├── director.md                    # Директор
│   ├── marshal.md                     # Маршал
│   └── ...                            # и остальные роли
├── scripts/                           # Скрипты сборки и публикации
│   ├── build_static.py                # Собирает HTML-сайт из Markdown
│   ├── publish_gist.py                # Публикация запасным способом (gist)
│   ├── setup_gist.sh
│   └── requirements.txt
├── static/
│   └── style.css                      # Оформление сайта
└── .github/workflows/                 # Автоматическая сборка и публикация
    ├── deploy-pages.yml               # GitHub Pages (основной способ)
    └── deploy-gist.yml                # Gist (запасной способ)
```

## Публикация сайта

**Рекомендуемый способ** — [GitHub Pages](https://pages.github.com/). При каждом push в `main` сайт собирается и публикуется автоматически:

**https://vutratenko.github.io/s95-kb/**

Никаких токенов и secrets не нужно — достаточно включить Pages в настройках репозитория (**Settings → Pages → Build and deployment → Source: GitHub Actions**), если это ещё не сделано.

### Другие варианты публикации

| Способ | Плюсы | Минусы | Когда использовать |
|--------|-------|--------|-------------------|
| **GitHub Pages** | Настоящий сайт по URL, бесплатно, без токенов | Нужен публичный репозиторий (или GitHub Pro для private) | **Основной вариант** |
| **Gist + HTML Preview** | Быстро, без настройки Pages | Не настоящий сайт, кривые URL, нужен токен `gist` | Запасной / встраивание |
| **Локально (`dist/`)** | Мгновенно, офлайн | Только у вас на компьютере | Разработка и проверка |
| **Cloudflare Pages / Netlify** | Свой домен, CDN | Отдельный сервис и настройка | Если нужен кастомный домен |

### Gist (запасной вариант)

Если нужен именно gist, ссылка для просмотра выглядит **не** как `gist.github.com/...`, а так:

```
https://htmlpreview.github.io/?https://gist.githubusercontent.com/vutratenko/f68341ac2d207e354fca576764e428c8/raw/index.html
```

Важно: в URL должен быть `gist.githubusercontent.com/.../raw/index.html`, а не страница gist.

Настройка gist (если используете workflow `Deploy to Gist`):

1. Создайте [Personal Access Token](https://github.com/settings/tokens) с правом `gist`.
2. Добавьте secrets `GIST_TOKEN` и `GIST_ID` в репозиторий.
3. Или выполните `./scripts/setup_gist.sh`.

## Локальная сборка

```bash
pip install -r scripts/requirements.txt
python scripts/build_static.py
```

Готовый сайт появится в каталоге `dist/`. Откройте `dist/index.html` в браузере, чтобы посмотреть результат. Для ручной публикации в gist:

```bash
export GIST_TOKEN=...
export GIST_ID=...
python scripts/publish_gist.py
```
