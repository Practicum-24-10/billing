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
