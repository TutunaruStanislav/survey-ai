# Survey Application - Мини-анкета

Простое веб-приложение для сбора обратной связи с использованием Python backend и vanilla JavaScript frontend.

## Функциональность

- **Backend**: Python HTTP server без внешних зависимостей
  - `GET /questions` — возвращает список из 5 вопросов анкеты
  - `POST /answers` — принимает и сохраняет ответы пользователя (in-memory storage)
  - `GET /docs` — интерактивная Swagger UI документация
  - `GET /openapi.yaml` — OpenAPI 3.0 спецификация

- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
  - Динамическая загрузка вопросов с backend
  - Поддержка различных типов вопросов (текст, radio-кнопки)
  - Отправка ответов на сервер
  - Отображение сообщения успешной отправки

## Технологический стек

- **Backend**: Python 3.14+ (только стандартная библиотека)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **API**: OpenAPI 3.0 + Swagger UI
- **Architecture**: Clean Architecture с разделением на models, services, handlers

## Структура проекта

```
survey/
├── backend/
│   ├── main.py                    # Точка входа, HTTP сервер
│   ├── models/
│   │   ├── __init__.py
│   │   ├── question.py            # Question dataclass
│   │   └── answer.py              # AnswerSubmission dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── survey_service.py      # Бизнес-логика + in-memory хранилище
│   └── handlers/
│       ├── __init__.py
│       ├── questions_handler.py   # GET /questions обработчик
│       └── answers_handler.py     # POST /answers обработчик
├── frontend/
│   ├── index.html                 # HTML форма
│   ├── style.css                  # Стили
│   └── script.js                  # Логика формы
├── openapi.yaml                   # API документация
└── README.md                       # Этот файл
```

## Установка и запуск

### Требования

- Python 3.8+
- Не требуется установка дополнительных зависимостей

### Запуск сервера

1. Перейдите в директорию проекта:

```bash
cd survey
```

2. Запустите сервер:

```bash
python run.py
```

Или напрямую из корневого каталога:

```bash
python survey/run.py
```

3. Откройте браузер и перейдите на:

- **Приложение**: http://127.0.0.1:9000
- **Swagger UI документация**: http://127.0.0.1:9000/docs
- **OpenAPI спецификация**: http://127.0.0.1:9000/openapi.yaml

## API Endpoints

### GET /questions

Возвращает список всех вопросов анкеты.

**Response (200 OK):**

```json
[
  {
    "id": "q1",
    "text": "Как вас зовут?",
    "type": "text",
    "options": []
  },
  {
    "id": "q3",
    "text": "Оцените качество курса",
    "type": "radio",
    "options": ["1", "2", "3", "4", "5"]
  }
]
```

### POST /answers

Сохраняет ответы пользователя.

**Request body:**

```json
{
  "q1": "John Doe",
  "q2": "25",
  "q3": "5",
  "q4": "Great course!",
  "q5": "Да"
}
```

**Response (200 OK):**

```json
{
  "success": true,
  "message": "Спасибо!",
  "submission": {
    "submission_id": "550e8400-e29b-41d4-a716-446655440000",
    "answers": {
      "q1": "John Doe",
      "q2": "25",
      "q3": "5",
      "q4": "Great course!",
      "q5": "Да"
    },
    "submitted_at": "2024-01-15T10:30:00Z"
  }
}
```

## Вопросы анкеты

1. **Как вас зовут?** (текстовое поле)
2. **Ваш возраст?** (текстовое поле)
3. **Оцените качество курса** (radio: 1, 2, 3, 4, 5)
4. **Что вам понравилось больше всего?** (текстовое поле)
5. **Рекомендовали бы вы этот курс другим?** (radio: Да, Нет, Возможно)

## Архитектура

### Models (models/)

- `Question` — представляет вопрос анкеты
- `AnswerSubmission` — представляет отправленные ответы с metadata

### Services (services/)

- `SurveyService` — бизнес-логика:
  - Хранит список вопросов
  - Управляет in-memory хранилищем ответов
  - Методы: `get_questions()`, `save_answers()`

### Handlers (handlers/)

- `handle_get_questions()` — обработчик GET /questions
- `handle_post_answers()` — обработчик POST /answers

### Frontend

- Загружает вопросы при загрузке страницы
- Динамически рендерит форму
- Отправляет ответы через fetch API
- Показывает сообщение успеха после отправки

## Примеры использования

### cURL

```bash
# Получить вопросы
curl http://127.0.0.1:9000/questions

# Отправить ответы
curl -X POST http://127.0.0.1:9000/answers \
  -H "Content-Type: application/json" \
  -d '{
    "q1": "Иван",
    "q2": "30",
    "q3": "5",
    "q4": "Отличный контент",
    "q5": "Да"
  }'
```

### JavaScript

```javascript
// Получить вопросы
const questions = await fetch('http://127.0.0.1:9000/questions')
  .then(r => r.json());

// Отправить ответы
const result = await fetch('http://127.0.0.1:9000/answers', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ q1: 'Иван', q2: '30', ... })
}).then(r => r.json());
```

## Хранилище данных

Все ответы хранятся в памяти приложения в виде словаря (dict):

```python
_storage = {
    'submission_id_1': AnswerSubmission(...),
    'submission_id_2': AnswerSubmission(...),
}
```

**Важно**: данные теряются при перезагрузке сервера!

## Развертывание

### Локальная разработка

```bash
python backend/main.py
```

Откройте http://127.0.0.1:9000

### Изменение порта

Отредактируйте `backend/main.py`, функция `run_server()`:

```python
def run_server(host='localhost', port=8008):
    # или используйте другой порт при вызове:
    # run_server(port=YOUR_PORT)
```

## Contributing

Проект создан как учебный пример. Для совершенствования:

1. Добавить базу данных (SQLite, PostgreSQL)
2. Добавить аутентификацию
3. Добавить валидацию данных
4. Добавить rate limiting
5. Улучшить обработку ошибок

## Лицензия

MIT
