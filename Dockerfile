FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install

# Seperate the install from the rest of the files to keep cached steps
COPY . /app 