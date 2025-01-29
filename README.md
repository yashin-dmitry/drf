## Описание

Этот проект представляет собой Django-приложение с использованием Celery и Celery Beat для выполнения фоновых задач.

## Предварительные требования

- Docker
- Docker Compose

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yashin-dmitry/drf.git

2. Соберите и запустите контейнеры:

docker-compose up --build

3. Доступ к приложению:

Откройте браузер и перейдите по адресу http://localhost:8000.

Проверка работоспособности сервисов

Backend: Убедитесь, что приложение Django работает, перейдя по адресу http://localhost:8000.
Database: Убедитесь, что база данных PostgreSQL работает, проверив логи в выводе Docker Compose.
Redis: Убедитесь, что Redis работает, проверив логи в выводе Docker Compose.
Celery: Убедитесь, что Celery worker работает, проверив логи в выводе Docker Compose.
Celery Beat: Убедитесь, что Celery Beat работает, проверив логи в выводе Docker Compose.