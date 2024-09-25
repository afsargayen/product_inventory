FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install poetry \
   && poetry install --no-dev

 CMD ["poetry", "run", "uvicorn", "main:app", "--reload"]