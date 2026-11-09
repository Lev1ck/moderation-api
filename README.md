# Ad Moderation API

FastAPI-сервис, определяющий наличие нарушения в объявлении.

`POST /predict` принимает JSON с полями `seller_id: int`, `is_verified_seller: bool`, `item_id: int`, `name: str`, `description: str`, `category: int`, `images_qty: int`.
Все поля обязательны. Типы проверяются строго, `images_qty >= 0`, дополнительные поля запрещены.

Результат — **одно JSON-значение boolean**:

- `true` — нарушение есть (продавец не подтверждён и нет изображений);
- `false` — нарушения нет (продавец подтверждён либо есть хотя бы одно изображение).

Поля `seller_id`, `item_id`, `name`, `description`, `category` пока не влияют на результат, но обязательны по контракту API.

## Установка и запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev
```

Для Windows активация: `.venv\Scripts\activate`.

После запуска: http://127.0.0.1:8000/docs

## Пример

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"seller_id":10,"is_verified_seller":false,"item_id":42,"name":"Bicycle","description":"Used bicycle","category":3,"images_qty":0}'
```

Ответ: `true` (HTTP 200).

Некорректные поля/отсутствующие поля: HTTP 400 с описанием ошибок. Ошибка сервиса: HTTP 500 с безопасным сообщением.

## Тесты

```bash
python -m pytest -q
```

## Структура

- `main.py` — приложение, роутер и обработчик ошибок валидации
- `routers/predict.py` — HTTP-обработчик и внедрение сервиса
- `schemas/moderation.py` — контракт запроса
- `services/moderation.py` — бизнес-логика
- `repositories/moderation.py` — источник параметра правила (пока in-memory, без БД)
- `tests/` — тесты HTTP API и сервиса
