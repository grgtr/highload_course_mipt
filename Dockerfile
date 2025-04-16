FROM python:3.10-slim

WORKDIR /app

# Копируем файл зависимостей ДО копирования остального кода
# Это позволяет Docker кешировать слой установки зависимостей,
# если requirements.txt не изменился
COPY requirements.txt ./

# Устанавливаем зависимости
# --no-cache-dir чтобы не хранить кеш pip, уменьшая размер образа
# --compile чтобы избежать компиляции при первом запуске
RUN pip install --no-cache-dir --compile -r requirements.txt

# Копируем остальной код приложения в рабочую директорию
COPY . .

# Указываем Flask, где искать приложение (хотя app.py и так запустится)
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0 # Чтобы было доступно снаружи контейнера

# Создаем директорию instance, если она не скопировалась (из-за .dockerignore)
# SQLAlchemy создаст ее сам, но лучше явно указать владельца
# RUN mkdir instance && chown nobody:nogroup instance
# Примечание: Управление `instance` лучше делать через volume в docker-compose

# Порт, который слушает Flask внутри контейнера
EXPOSE 5000
# Порт, который слушает Locust UI по умолчанию
EXPOSE 8089

# Команда по умолчанию для запуска приложения Flask
# Используем gunicorn или waitress для более продакшн-готового варианта,
# но для ДЗ хватит и встроенного сервера Flask.
# Важно: host='0.0.0.0' в app.py обязателен для Docker.
CMD ["python", "app.py"]

# Альтернативная команда для запуска (если бы не использовали CMD в compose):
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"] # Требует pip install gunicorn