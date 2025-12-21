FROM python:3.12

WORKDIR /code

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry &&  \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]