FROM python:3.13.2-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY backend .

COPY backend/.env.docker .env

COPY requirements.txt .

# Экономим дисковое пространство: для сборки драйвера asyncmy нужен gcc и пачка либ к нему. Если разбить эту строку
# на три красивых и логичных RUN - докер их закэширует и увеличит образ до 700мб, с одной страшной строкой - образ 250мб
RUN apk update && apk add python3-dev gcc libc-dev libffi-dev && pip install -r requirements.txt && apk del python3-dev gcc libc-dev libffi-dev

RUN chmod +x run_or_migrate.sh

EXPOSE 8000

ENTRYPOINT ["./run_or_migrate.sh"]
