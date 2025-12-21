FROM python:3.12-slim

WORKDIR /code

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /code
USER appuser

EXPOSE 8000

CMD ["bash", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application"]

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]