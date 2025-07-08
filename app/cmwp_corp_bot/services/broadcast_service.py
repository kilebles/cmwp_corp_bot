# app/cmwp_corp_bot/services/broadcast_service.py
import asyncio
from typing import Sequence

from sqlalchemy import select
from aiogram.exceptions import TelegramRetryAfter

from app.cmwp_corp_bot.db.repo import get_session
from app.cmwp_corp_bot.db.models import (
    User, Mailing, MailingSend, MediaKind, SendStatus,
)
from app.cmwp_corp_bot.dispatcher import bot


async def _broadcast(mailing_id: int) -> None:
    """Разослать выбранную рассылку всем пользователям в Telegram."""
    async with get_session() as s:
        mailing: Mailing | None = await s.get(Mailing, mailing_id)
        if mailing is None:
            return

    async with get_session() as s:
        users: Sequence[User] = list(await s.scalars(select(User)))

    for user in users:
        try:
            if mailing.media_kind is MediaKind.PHOTO and mailing.media_url:
                await bot.send_photo(user.tg_id, mailing.media_url,
                                     caption=mailing.text)
            elif mailing.media_kind is MediaKind.VIDEO and mailing.media_url:
                await bot.send_video(user.tg_id, mailing.media_url,
                                     caption=mailing.text)
            else:
                await bot.send_message(user.tg_id, mailing.text)

            status = SendStatus.SENT

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            status = SendStatus.PENDING

        except Exception:
            status = SendStatus.FAILED

        # фиксируем результат
        async with get_session() as s:
            s.add(MailingSend(
                mailing_id=mailing_id,
                user_id=user.id,
                status=status,
            ))


def send_broadcast_by_id(mailing_id: int) -> None:
    asyncio.run(_broadcast(mailing_id))
