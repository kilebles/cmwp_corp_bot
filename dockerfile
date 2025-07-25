FROM python:3.11-slim

RUN apt-get update && apt-get install -y build-essential gcc && apt-get clean

ENV LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction

COPY . .

CMD ["python", "app/cmwp_corp_bot/main.py"]
