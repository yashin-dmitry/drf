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


# Django Project Deployment Guide

## Настройка удаленного сервера

### Подготовка сервера

1. **Выбор провайдера**: Выберите провайдера для удаленного сервера (например, Yandex Cloud).
2. **Создание сервера**: Создайте новый сервер (инстанс) с выбранным провайдером.

### Установка необходимых пакетов

1. **Подключение к серверу**: Подключитесь к серверу через SSH.
ssh username@server_ip

2. **Обновление пакетов**: Обновите пакеты до последней версии.
sudo apt update
sudo apt upgrade

3. **Установка Python**: Установите Python и необходимые зависимости.
sudo apt install python3 python3-pip python3-venv

4. **Установка и активация виртуального окружения**: Установите и активируйте виртуальное окружение.
python3 -m venv /home/dmitry/drfclone2/venv
source /home/dmitry/drfclone2/venv/bin/activate

5. **Установка Django и других зависимостей**: Установите Django, Django REST Framework и Gunicorn. 
pip install django djangorestframework gunicorn

6. **Установка Nginx**: Установите Nginx для обработки HTTP-запросов.
sudo apt install nginx


### Настройка Nginx

1. **Создание конфигурации Nginx**: Создайте файл конфигурации для вашего проекта.
sudo nano /etc/nginx/sites-available/drfclone2

2. **Создание символической ссылки**: Создайте символическую ссылку на файл конфигурации.
sudo ln -s /etc/nginx/sites-available/drfclone2 /etc/nginx/sites-enabled

3. **Перезапуск Nginx**: Перезапустите Nginx для применения изменений. 
sudo systemctl restart nginx


### Настройка Gunicorn

1. **Создание файла сервиса systemd**: Создайте файл сервиса для управления Gunicorn.
sudo nano /etc/systemd/system/drfclone2.service

2. **Перезагрузка systemd**: Перезагрузите systemd для применения изменений.
sudo systemctl daemon-reload

3. **Запуск и включение сервиса**: Запустите сервис и включите его для автоматического запуска при старте системы.
sudo systemctl start drfclone2
sudo systemctl enable drfclone2

4. **Проверка статуса сервиса**: Проверьте статус сервиса, чтобы убедиться, что он работает корректно.
sudo systemctl status drfclone2


### Настройка параметров безопасности

1. **Закрытие ненужных портов**: Используйте `ufw` для настройки брандмауэра и закрытия ненужных портов.
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable

2. **Использование SSH-ключей**: Настройте доступ по SSH-ключам, отключив доступ по паролю.


## Настройка переменных окружения

1. **Создание файла `.env.example`**: Создайте файл `.env.example` с примерами переменных окружения.
2. **Создание файла `.env` на сервере**: Скопируйте файл `.env.example` в `.env` и заполните его реальными значениями.
3. **Установка пакета `python-dotenv`**: Установите пакет `python-dotenv` для загрузки переменных окружения.
4. **Настройка Django для использования `.env`**: Настройте Django для загрузки переменных окружения из файла `.env`.

## Настройка GitHub Actions

1. **Создание файла workflow**: Создайте файл `deploy.yml` в директории `.github/workflows`.
2. **Настройка шагов workflow**: Настройте шаги для запуска тестов и деплоя приложения на сервер.
3. **Добавление секретов в GitHub**: Добавьте необходимые секреты в настройки репозитория на GitHub.

## Проверка работы приложения

1. **Проверка доступности приложения**: Убедитесь, что ваше приложение доступно через Nginx.
http://84.201.165.84

2. **Проверка работы сервиса**: Убедитесь, что сервис Gunicorn работает корректно.
sudo systemctl status drfclone2
Проверьте логи сервиса для получения дополнительной информации:
sudo journalctl -u drfclone2
Убедитесь, что сокет Gunicorn существует и доступен:
ls -l /home/dmitry/drfclone2/drfclone2.sock
