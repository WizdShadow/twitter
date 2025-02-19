# Указываем базовый образ, который будет использоваться для сборки контейнера
FROM python:3.10

# Устанавливаем рабочие каталоги внутри контейнера
WORKDIR /app

# Копируем все файлы из текущего каталога в рабочий каталог контейнера
COPY . .

# Устанавливаем необходимые пакеты из файла requirements.txt

RUN touch /app/.env
RUN pip install -r reg.txt
RUN echo "DATABASE_URL_TEST_SYNC=postgresql+asyncpg://postgres:mysecretpassword@db:5342/twitter_test" >> /app/.env
RUN echo "DATABASE_URL_TEST=postgresql+asyncpg://postgres:mysecretpassword@db:5342/twitter_test" >> /app/.env

# Открываем порт 8000 для доступа к приложению снаружи контейнера
EXPOSE 8000

