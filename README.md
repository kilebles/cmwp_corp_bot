cmwp_corp_bot Telegram-бот Реализован на aiogram 3.x на полинге и с Django-админкой. Поддерживает smtp рассылку, рассылку по пользователям, фильтрацию по действиям.

## Запуск

1. Применить миграции Alembic:

    ```bash
    alembic upgrade head
    ```

2. Настроить Django-админку:

    ```bash
    docker compose exec django_admin bash
    python app/admin/manage.py makemigrations
    python app/admin/manage.py migrate
    python app/admin/manage.py createsuperuser
    ```

## .env.example

```
BOT_TOKEN=

POSTGRES_HOST=
POSTGRES_PORT=5432
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

EMAIL_ADRESS=
SMTP_USER=
SMTP_PASS=
```