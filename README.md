# billing

## Первый запуск

1) Сформируй виртуальное Python-окружение
2) Установи зависимости `pip install -r requirements.txt`
3) Установи pre-commit hook `pre-commit install`

## Линтер

Используется `flake8`.

Конфигурация находится в `pyproject.toml`

Запуск: `flake8`

## Проверка типов

Используется `pyright`.

Конфигурация находится в `pyproject.toml`

Запуск: `pyright`

## CI-CD

В GitHub actions настроен запуск линтера и прверка типов.

### Запуск тестов backend в контейнере
- Создайте файл .env по примеру .env.example и tests/.env по примеру tests/.env.example, выполнить команду:
```
docker compose -f backend/tests/functional/docker-compose.yml up
```

### Запуск тестов backend в локально
- Создать файл .env по примеру .env.example и tests/.env по примеру tests/.env.example, выполнить команду:
```
docker compose -f backend/tests/functional/docker-compose.dev.yml up
```

