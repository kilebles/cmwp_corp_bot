from __future__ import annotations

from typing import TypedDict

import sqlalchemy as sa
from aiogram.types import User as TgUser

from app.cmwp_corp_bot.db.models import User
from app.cmwp_corp_bot.db.repo import get_session


class RegData(TypedDict):
    """Данные, собранные в FSM-регистрации."""
    tg_user: TgUser
    full_name: str
    company: str
    position: str
    phone: str
    email: str


async def save_registration(data: RegData) -> None:
    async with get_session() as session:
        exists = await session.scalar(
            sa.select(User.id).where(User.tg_id == data["tg_user"].id)
        )
        if exists:
            return

        session.add(
            User(
                tg_id=data["tg_user"].id,
                full_name=data["full_name"],
                company=data["company"],
                position=data["position"],
                phone=data["phone"],
                email=data["email"],
            )
        )


async def user_exists(tg_id: int) -> bool:
    """Проверяем, есть ли уже пользователь"""
    async with get_session() as session:
        return await session.scalar(
            sa.select(User.id).where(User.tg_id == tg_id).limit(1)
        ) is not None