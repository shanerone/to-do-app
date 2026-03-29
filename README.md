# To‑Do App — Backend (FastAPI)

### Коротко
-------
*Учебный backend для To‑Do приложения на FastAPI + SQLAlchemy (async).  
Проект предназначен для локальной разработки и интеграции с простым фронтендом.  
В этом README — инструкции по установке, запуску, базовые API-примеры.*

### Структура
-----------------
- `main.py` — точка входа FastAPI
- `db/` — подключение к БД, create_tables/get_db
- `models/` — ORM-модели
- `repositories/` — слой доступа к данным
- `schemas/` — Pydantic-схемы
- `docs/screenshots/` — место для скриншотов фронтенда

Требования
----------
- Python 3.10+ (рекомендуется 3.11)
- PostgreSQL (локально или в контейнере)
- Для фронтенда — Node.js (если запускаете фронт)
- Установленные зависимости: `pip install -r requirements.txt`

Быстрая установка и запуск (локально)
------------------------------------
1) Создать виртуальное окружение и установить зависимости:  
```
python -m venv .venv  
на MacOS source .venv/bin/activate  
на Windows: .venv\Scripts\activate  
pip install -r requirements.txt
```

2) Указать базовый URL БД (в окружении или в `.env`):
```
Пример 
DATABASE_URL=postgresql+asyncpg://postgres:admin@127.0.0.1:15432/postgres
```

3) Запустить сервер
```Stazirovka/todo_app_backend/README.md#L18-19
uvicorn main:app --reload 
```

API — основные эндпоинты
-----------------------
### 1) Получить список задач (`GET /tasks`)

Тело запроса: **отсутствует**.

Ожидаемый ответ:
- Статус: `200 OK`
- Тело ответа: JSON-массив задач

```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Сделать ДЗ",
    "completed": false
  },
  {
    "id": "f4d8d97d-27b2-4f74-9c14-f1f8ee9b9d4f",
    "title": "Написать Пет-Проект",
    "completed": true
  }
]
```

Если задач нет:

```json
[]
```
<img src="data/get.png" alt="GET пустой список" width="800" />

### 2) Создать задачу (`POST /tasks`)

Тело запроса:

```json
{
  "title": "Написать README"
}
```

Ожидаемый ответ:
- Статус: `201 Created` (допустимо `200 OK`)
- Тело ответа: созданная задача

```json
{
  "id": "b1b3d9d7-7d47-4f30-a9f6-9dce7d8f43d2",
  "title": "Написать README",
  "completed": false
}
```
<img src="data/post.png" alt="GET пустой список" width="800" />
### 3) Обновить задачу (`PATCH /tasks/{id}`)

`id` в path-параметре: строковый UUID.

Тело запроса: только изменившиеся поля (одно или несколько).

Если поменялся только `title`:

```json
{
  "title": "Подготовиться к контрольной"
}
```

Если поменялся только `completed`:

```json
{
  "completed": true
}
```

Если поменялись оба поля:

```json
{
  "title": "Подготовиться к контрольной",
  "completed": true
}
```

Ожидаемый ответ:
- Статус: `200 OK`
- Тело ответа: обновленная задача

```json
{
  "id": "b1b3d9d7-7d47-4f30-a9f6-9dce7d8f43d2",
  "title": "Подготовиться к контрольной",
  "completed": true
}
```
<img src="data/patch.png" alt="GET пустой список" width="800" />
### 4) Удалить задачу (`DELETE /tasks/{id}`)

`id` в path-параметре: строковый UUID.

Тело запроса: **отсутствует**.

Ожидаемый ответ:
- Статус: `204 No Content`
- Тело ответа: **отсутствует**

<img src="data/get.png" alt="GET пустой список" width="800" />

Документация API (Swagger)
--------------------------
После запуска сервера открой:
- http://127.0.0.1:8080/docs — Swagger UI
- http://127.0.0.1:8080/redoc — Redoc

Еще нужно доделать «Категории» для группировки задач.