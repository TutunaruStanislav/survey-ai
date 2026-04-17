# Структура проекта Survey Application

## Обзор

Мини-приложение анкеты с чистой архитектурой, разделенной на:
- **Backend**: Python HTTP server (стандартная библиотека)
- **Frontend**: Vanilla HTML5/CSS3/JavaScript
- **API Documentation**: OpenAPI 3.0 + Swagger UI

## Древо файлов

```
survey/
├── run.py                           # Точка входа (запуск сервера)
├── requirements.txt                 # Зависимости (нет)
├── .gitignore                       # Исключения для git
├── README.md                        # Документация проекта
├── STRUCTURE.md                     # Этот файл
├── openapi.yaml                     # OpenAPI 3.0 спецификация
│
├── backend/                         # Backend Python приложение
│   ├── __init__.py
│   ├── main.py                      # HTTP server (ThreadingHTTPServer)
│   │                                 # - GET /questions
│   │                                 # - POST /answers
│   │                                 # - GET /docs (Swagger UI)
│   │                                 # - GET /openapi.yaml
│   │                                 # - GET / и статика
│   │
│   ├── models/                      # Data models (dataclasses)
│   │   ├── __init__.py
│   │   ├── question.py              # Question(id, text, type, options)
│   │   └── answer.py                # AnswerSubmission(id, answers, timestamp)
│   │
│   ├── services/                    # Business logic layer
│   │   ├── __init__.py
│   │   └── survey_service.py        # SurveyService с 5 вопросами + in-memory storage
│   │
│   └── handlers/                    # HTTP request handlers
│       ├── __init__.py
│       ├── questions_handler.py     # GET /questions обработчик
│       └── answers_handler.py       # POST /answers обработчик
│
└── frontend/                        # Frontend веб-приложение
    ├── index.html                   # HTML структура
    ├── style.css                    # Стили (современный дизайн)
    └── script.js                    # Логика формы (fetch API)
```

## Компоненты

### Backend Architecture

```
HTTP Request
    ↓
main.py (SurveyHandler)
    ↓
Routing (GET/POST)
    ↓
handlers/
├── questions_handler.py → Service.get_questions()
└── answers_handler.py → Service.save_answers()
    ↓
services/survey_service.py
├── get_questions() → list[Question]
└── save_answers() → AnswerSubmission (in-memory)
    ↓
models/
├── Question (dataclass)
└── AnswerSubmission (dataclass)
```

### Frontend Workflow

```
Browser
    ↓
index.html (loads style.css + script.js)
    ↓
script.js DOMContentLoaded
    ↓
fetchQuestions() → GET /questions
    ↓
renderForm() (dynamic form generation)
    ↓
submitForm() → POST /answers
    ↓
Show "Спасибо!" message
```

## API Endpoints

### GET /questions
Возвращает массив 5 вопросов в формате JSON:
```json
[
  {"id": "q1", "text": "...", "type": "text", "options": []},
  {"id": "q3", "text": "...", "type": "radio", "options": ["1", "2", "3", "4", "5"]},
  ...
]
```

### POST /answers
Принимает объект с ответами:
```json
{
  "q1": "ответ1",
  "q2": "ответ2",
  ...
}
```

Возвращает:
```json
{
  "success": true,
  "message": "Спасибо за ответы!",
  "submission": {
    "submission_id": "uuid",
    "answers": {...},
    "submitted_at": "ISO timestamp"
  }
}
```

### GET /docs
Интерактивная Swagger UI документация (через CDN).

### GET /openapi.yaml
Файл спецификации OpenAPI 3.0.

## Вопросы анкеты

1. **Как вас зовут?** (text)
2. **Ваш возраст?** (text)
3. **Оцените качество курса** (radio: 1-5)
4. **Что вам понравилось больше всего?** (text)
5. **Рекомендовали бы вы курс другим?** (radio: Да/Нет/Возможно)

## Запуск

```bash
# Из папки survey/
python run.py

# Открыть в браузере:
# - Приложение: http://127.0.0.1:9000
# - Swagger UI: http://127.0.0.1:9000/docs
# - OpenAPI: http://127.0.0.1:9000/openapi.yaml
```

## Чистая архитектура

✓ **Models**: Независимые dataclasses (Question, AnswerSubmission)
✓ **Services**: Бизнес-логика (SurveyService) без зависимостей от框架
✓ **Handlers**: Тонкий слой для HTTP обработки
✓ **Main**: Сборка компонентов и маршрутизация

Разделение позволяет:
- Легко тестировать бизнес-логику (SurveyService)
- Заменять хранилище (in-memory → БД)
- Переиспользовать сервис в других контекстах
- Добавлять новые endpoints без изменения существующего кода

## Технологический стек

- **Backend**: Python 3.8+ (только stdlib)
- **Frontend**: HTML5 + CSS3 + Vanilla JS (ES6+)
- **API**: OpenAPI 3.0
- **Server**: http.server + socketserver.ThreadingTCPServer
- **Storage**: In-memory dict (UUID indexed)

## Без внешних зависимостей

- Нет pip-пакетов (Flask, FastAPI, и т.д.)
- Использует только стандартную библиотеку Python
- Frontend на чистом JavaScript (без фреймворков)
- Swagger UI подключается через CDN

## Развитие проекта

Возможные улучшения:
1. Добавить SQLite/PostgreSQL вместо in-memory
2. Добавить authentication (JWT tokens)
3. Добавить input validation (pydantic-like)
4. Добавить rate limiting
5. Добавить тесты (unittest)
6. Добавить logging
7. Добавить CORS middleware
8. Контейнеризация (Docker)
