FROM python:3.12-slim

WORKDIR /app

RUN apt-get update  \
    && apt-get install -y libpq-dev gcc  \
    && apt-get clean  \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем и даём права на папку со статикой
RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]