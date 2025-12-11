FROM python:3.13.2

WORKDIR /code

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry &&  \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]