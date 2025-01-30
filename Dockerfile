# Указываем базовый образ
FROM python:3.10-slim

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /code

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменные окружения из .env файла
RUN python -m pip install python-dotenv

# Копируем остальные файлы проекта в контейнер
COPY . /code/

# Устанавливаем права доступа для файлов
RUN chmod +x /code/manage.py

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
