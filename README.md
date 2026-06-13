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

## Статический хостинг на GitHub Gist

При каждом push в `main` GitHub Actions собирает HTML-версию базы знаний и публикует её в [GitHub Gist](https://gist.github.com/).

### Быстрая настройка одной командой

Если у вас есть [Personal Access Token](https://github.com/settings/tokens) с правом `gist`, выполните в корне репозитория:

```bash
export GITHUB_TOKEN=ghp_ваш_токен
chmod +x scripts/setup_gist.sh
./scripts/setup_gist.sh
```

Скрипт создаст gist, опубликует сайт и попытается добавить `GIST_TOKEN` и `GIST_ID` в secrets репозитория.

### Настройка вручную

1. Создайте **публичный** gist на [gist.github.com](https://gist.github.com/) — можно с любым файлом-заглушкой.
2. Скопируйте **ID** gist из адреса: `https://gist.github.com/<user>/<gist_id>`.
3. Создайте [Personal Access Token](https://github.com/settings/tokens) с правом `gist`.
4. В настройках репозитория (**Settings → Secrets and variables → Actions**) добавьте секреты:
   - `GIST_TOKEN` — токен с правом `gist`
   - `GIST_ID` — ID gist

После следующего push в `main` workflow обновит gist автоматически.

### Просмотр сайта

GitHub отдаёт HTML из gist как исходный текст, поэтому для просмотра в браузере используйте превью:

```
https://htmlpreview.github.io/?https://gist.githubusercontent.com/<user>/<gist_id>/raw/index.html
```

Замените `<user>` и `<gist_id>` на свои значения. Ссылку на gist можно также взять в логах workflow после успешного деплоя.

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
