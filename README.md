# To‑Do App — Backend (FastAPI)

-------
*Учебный backend для To‑Do приложения на FastAPI + SQLAlchemy (async).  
Проект предназначен для локальной разработки и интеграции с простым фронтендом.  
В этом README — инструкции по установке, запуску, базовые API-примеры.*

---

## Структура
-----------------
- `main.py` — точка входа FastAPI
- `db/` — подключение к БД, create_tables/get_db
- `models/` — ORM-модели
- `repositories/` — слой доступа к данным
- `schemas/` — Pydantic-схемы
- `routers/` — маршруты для задач, категорий и аутентификации
- `auth/` — логика аутентификации (JWT, хэширование паролей)
- `docs/screenshots/` — место для скриншотов фронтенда

---

## Требования
----------
- Python 3.10+ (рекомендуется 3.11)
- PostgreSQL (локально или в контейнере)
- Установленные зависимости: `pip install -r requirements.txt`

---

## Быстрая установка и запуск (локально)
------------------------------------
1. Создать виртуальное окружение и установить зависимости:  
```bash
python -m venv .venv  
source .venv/bin/activate  # MacOS/Linux  
.venv\Scripts\activate     # Windows  
pip install -r requirements.txt
```

2. Указать базовый URL БД (в окружении или в `.env`):
```env
DATABASE_URL=postgresql+asyncpg://postgres:admin@127.0.0.1:15432/postgres
SECRET_KEY=your_secret_key
```

3. Запустить сервер:
```bash
uvicorn main:app --reload 
```

---

## API — основные эндпоинты

### 1) Аутентификация

#### Регистрация (`POST /auth/register`)
Тело запроса:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Ожидаемый ответ:
- Статус: `201 Created`
- Тело ответа:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "email": "user@example.com"
}
```

#### Логин (`POST /auth/login`)
Тело запроса:
```json
{
  "username": "user@example.com",
  "password": "securepassword"
}
```

Ожидаемый ответ:
- Статус: `200 OK`
- Тело ответа:
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

#### Получение текущего пользователя (`GET /auth/me`)
Ожидаемый ответ:
- Статус: `200 OK`
- Тело ответа:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "email": "user@example.com"
}
```

---

### 2) Задачи

#### Получить список задач (`GET /tasks`)
Тело запроса: **отсутствует**.

Ожидаемый ответ:
```json
[
  {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "title": "Сделать ДЗ",
    "completed": false,
    "category_id": "f4d8d97d-27b2-4f74-9c14-f1f8ee9b9d4f"
  }
]
```

#### Создать задачу (`POST /tasks`)
Тело запроса:
```json
{
  "title": "Написать README",
  "category_id": "f4d8d97d-27b2-4f74-9c14-f1f8ee9b9d4f"
}
```

Ожидаемый ответ:
```json
{
  "id": "b1b3d9d7-7d47-4f30-a9f6-9dce7d8f43d2",
  "title": "Написать README",
  "completed": false,
  "category_id": "f4d8d97d-27b2-4f74-9c14-f1f8ee9b9d4f"
}
```

#### Обновить задачу (`PATCH /tasks/{id}`)
Тело запроса:
```json
{
  "title": "Подготовиться к контрольной",
  "completed": true
}
```

Ожидаемый ответ:
```json
{
  "id": "b1b3d9d7-7d47-4f30-a9f6-9dce7d8f43d2",
  "title": "Подготовиться к контрольной",
  "completed": true,
  "category_id": "f4d8d97d-27b2-4f74-9c14-f1f8ee9b9d4f"
}
```

#### Удалить задачу (`DELETE /tasks/{id}`)
Ожидаемый ответ:
- Статус: `204 No Content`

---

### 3) Категории

#### Получить список категорий (`GET /categories`)
Ожидаемый ответ:
```json
[
  {
    "id": "f4d8d97d-27b2-4f74-9c14-f1f8ee9b9d4f",
    "title": "Работа",
    "color": "#b98b43"
  }
]
```

#### Создать категорию (`POST /categories`)
Тело запроса:
```json
{
  "title": "Учеба",
  "color": "#ff5733"
}
```

Ожидаемый ответ:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Учеба",
  "color": "#ff5733"
}
```

#### Обновить категорию (`PATCH /categories/{id}`)
Тело запроса:
```json
{
  "title": "Личное"
}
```

Ожидаемый ответ:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "title": "Личное",
  "color": "#ff5733"
}
```

#### Удалить категорию (`DELETE /categories/{id}`)
Ожидаемый ответ:
- Статус: `204 No Content`

---
<h2 align="center">🏞️ Screenshot</h2>

<img src="data/registr.png" alt="Вход и регистрация">

<br/>

<img src="data/zadachki.png" alt="Как выглядят задачи">

<br/>

<img src="data/category.png" alt="Как выглядят категории">

## Документация API (Swagger)
После запуска сервера открой:
- [Swagger UI](http://127.0.0.1:8000/docs)
- [Redoc](http://127.0.0.1:8000/redoc)

---

## Что сделано
- **Регистрация и аутентификация**: Добавлена возможность регистрации пользователей и авторизации через JWT.
- **Категории**: Теперь задачи можно распределять по категориям.
- **Типизация**: Улучшена типизация данных с использованием Pydantic.

---

## Планы на будущее
- Улучшение тестового покрытия.
- Добавление фильтров и сортировки задач.
- Реализация уведомлений для задач.


