# Tron Wallet Info API

Микросервис, который выводит информацию о кошельке в сети Tron. Информация включает в себя баланс TRX, bandwidth и energy. Микросервис принимает адрес кошелька и записывает запросы в базу данных.

## Описание проекта

Сервис состоит из двух эндпоинтов:

- **POST /wallet/request** — принимает адрес кошелька в сети Tron, делает запрос к сети Tron и сохраняет данные в базу данных.
- **GET /wallet/get_wallets_requests_list** — возвращает список последних запросов с пагинацией.

### Основные технологии:
- **Python** 3.12
- **FastAPI** — фреймворк для создания API
- **SQLAlchemy ORM** — для работы с базой данных
- **Alembic** — для миграций базы данных
- **Pydantic** — для валидации данных
- **Tronpy** — для взаимодействия с сетью Tron
- **Pytest** — для тестирования
- **Docker** — для контейнеризации и развертывания

## Установка

### Вариант 1: Локальная установка

1. **Клонирование репозитория**

   Для начала клонируйте репозиторий:

   ```bash
   git clone git@github.com:CostGamer/tron-wallet-info-api.git
   cd tron-wallet-info-api
   ```

2. **Установка зависимостей**

   Убедитесь, что у вас установлен **Poetry** для управления зависимостями.

   - Установите зависимости с помощью **Poetry**:

   ```bash
   poetry install
   ```

   - Активируйте виртуальное окружение:

   ```bash
   poetry shell
   ```

3. **Установка pre-commit хуков (dev режим)**

   Для установки pre-commit хуков, используйте следующую команду:

   ```bash
   pre-commit install
   ```

4. **Настройка базы данных**

   Для локальной работы с базой данных можно использовать Docker. Запустите PostgreSQL с помощью следующей команды:

   ```bash
   docker run --env-file=.env -p 127.0.0.1:5432:5432 -d postgres:alpine
   ```

5. **Создание переменных окружения**

   Создайте файл `.env` на примере `.env.example`

6. **Запуск приложения**

   Для запуска приложения выполните команду:

   ```bash
   ./starts.sh
   ```

Сервис будет доступен на `localhost:8000`.

### Вариант 2: Установка через Docker

1. **Создание переменных окружения**

   Создайте файл `.env` на примере `.env.example`

2. **Запуск приложения через Docker Compose**

   Если вы хотите запустить приложение с помощью Docker, просто выполните следующую команду:

   ```bash
   docker-compose up --build -d
   ```

Сервис будет доступен на `localhost:5000`.

## Миграции базы данных

Для применения миграций базы данных используйте следующую команду:

```bash
alembic upgrade head
```

## Тестирование

Проект включает в себя юнит-тесты и интеграционные тесты с использованием **pytest**. Для запуска тестов выполните:

```bash
pytest -p no:warnings -v #без warning
```
```bash
pytest -v 
```

## Структура проекта

```bash
├── src                     # Основной каталог с исходным кодом
│   ├── api                 # Маршруты FastAPI и зависимости
│   ├── core                # Общие зависимости
│   ├── DB                  # Работа с базой данных
│   │   └── migrations      # Alembic миграции
│   ├── middleware          # Пользовательские middleware
│   ├── repositories        # Репозитории для работы с БД
│   ├── services            # Бизнес-логика
│   └── main.py             # Точка входа FastAPI приложения
├── tests                   # Тесты (юнит, интеграционные)
├── .env.example            # Пример конфигурации окружения
├── .github/workflows       # CI/CD пайплайны
├── .pre-commit-config.yaml # Конфигурация pre-commit хуков
├── docker-compose.yml      
├── Dockerfile              
├── poetry.lock             # Файл блокировки Poetry
├── pyproject.toml          # Конфигурация Poetry
└── start.sh                # Скрипт для локального запуска
```

## Контакты

Если у вас возникли вопросы или предложения, можете связаться с нами по почте: `vladimirbryzgalov00@gmail.com`.
