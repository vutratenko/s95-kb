# s95-kb

База знаний сообщества С95 — о людях, благодаря которым каждую субботу в 9 утра случается забег на 5 км. Здесь по-человечески, без канцелярита, рассказано, чем занимаются волонтёры и из чего складывается субботнее утро.

Не знаете, с чего начать? Загляните в [общее описание волонтёрства](general/overview.md) — а дальше выбирайте роль по душе.

## Структура файлов

```
.
├── README.md
├── general/
│   └── overview.md                    # Общее описание волонтёрства и таблица ролей
└── roles/
    ├── director.md                    # Директор
    ├── marshal.md                     # Маршал
    ├── timer.md                       # Секундомер
    ├── photograph.md                  # Фотограф
    ├── tokens.md                      # Раздача карточек позиций
    ├── scanner.md                     # Сканер
    ├── instructor.md                  # Инструктаж новичков
    ├── marking_maker.md               # Разметка трассы
    ├── event_closer.md                # Замыкающий
    ├── marking_picker.md              # Сбор разметки
    ├── cards_sorter.md                # Сортировка карточек
    ├── bike_leader.md                 # Ведущий велосипед
    ├── pacemaker.md                   # Пейсмейкер
    ├── results_handler.md             # Обработка результатов
    ├── equipment_supplier.md          # Доставка оборудования
    ├── public_relations.md            # Связи с общественностью
    ├── warm_up.md                     # Проведение разминки
    ├── other.md                       # Разное
    ├── attendant.md                   # Сопровождающий
    ├── finish_maker.md                # Организация финиша
    ├── volunteer_coordinator.md       # Координатор волонтёров
    ├── food_maker.md                  # Организация питания
    ├── videographer.md                # Видеограф
    ├── designer.md                    # Дизайнер
    └── event_preparation.md           # Подготовка забега
```

## Роли волонтёров

| Статья | Название |
|--------|----------|
| [director.md](roles/director.md) | Директор |
| [marshal.md](roles/marshal.md) | Маршал |
| [timer.md](roles/timer.md) | Секундомер |
| [photograph.md](roles/photograph.md) | Фотограф |
| [tokens.md](roles/tokens.md) | Раздача карточек позиций |
| [scanner.md](roles/scanner.md) | Сканер |
| [instructor.md](roles/instructor.md) | Инструктаж новичков |
| [marking_maker.md](roles/marking_maker.md) | Разметка трассы |
| [event_closer.md](roles/event_closer.md) | Замыкающий |
| [marking_picker.md](roles/marking_picker.md) | Сбор разметки |
| [cards_sorter.md](roles/cards_sorter.md) | Сортировка карточек |
| [bike_leader.md](roles/bike_leader.md) | Ведущий велосипед |
| [pacemaker.md](roles/pacemaker.md) | Пейсмейкер |
| [results_handler.md](roles/results_handler.md) | Обработка результатов |
| [equipment_supplier.md](roles/equipment_supplier.md) | Доставка оборудования |
| [public_relations.md](roles/public_relations.md) | Связи с общественностью |
| [warm_up.md](roles/warm_up.md) | Проведение разминки |
| [other.md](roles/other.md) | Разное |
| [attendant.md](roles/attendant.md) | Сопровождающий |
| [finish_maker.md](roles/finish_maker.md) | Организация финиша |
| [volunteer_coordinator.md](roles/volunteer_coordinator.md) | Координатор волонтёров |
| [food_maker.md](roles/food_maker.md) | Организация питания |
| [videographer.md](roles/videographer.md) | Видеограф |
| [designer.md](roles/designer.md) | Дизайнер |
| [event_preparation.md](roles/event_preparation.md) | Подготовка забега |

## Сайт

**Рекомендуемый способ** — [GitHub Pages](https://pages.github.com/). При каждом push в `main` сайт собирается и публикуется автоматически:

**https://vutratenko.github.io/s95-kb/**

### Первый запуск (один раз)

Деплой упадёт с ошибкой `404`, пока Pages не включён. Сделайте один раз:

1. Откройте [настройки Pages](https://github.com/vutratenko/s95-kb/settings/pages)
2. **Build and deployment → Source** → выберите **GitHub Actions**
3. Перезапустите workflow: [Deploy GitHub Pages → Run workflow](https://github.com/vutratenko/s95-kb/actions/workflows/deploy-pages.yml)

После этого сайт появится по адресу выше (обычно через 1–2 минуты).

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

### Локальная сборка

```bash
pip install -r scripts/requirements.txt
python scripts/build_static.py
```

Готовый сайт появится в каталоге `dist/`. Для ручной публикации:

```bash
export GIST_TOKEN=...
export GIST_ID=...
python scripts/publish_gist.py
```
