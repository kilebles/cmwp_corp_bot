import asyncio
from typing import Sequence

from sqlalchemy import select
from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter

from app.cmwp_corp_bot.settings import config
from app.cmwp_corp_bot.db.repo import get_session
from app.cmwp_corp_bot.db.models import (
    User, Mailing, MailingSend, MediaKind, SendStatus,
)


async def _broadcast(mailing_id: int) -> None:
    async with get_session() as s:
        mailing: Mailing | None = await s.get(Mailing, mailing_id)
        users: Sequence[User] = list(await s.scalars(select(User)))
    if not mailing or not users:
        return

    async with Bot(token=config.BOT_TOKEN, parse_mode="HTML") as bot:
        for user in users:
            try:
                if mailing.media_kind is MediaKind.PHOTO and mailing.media_url:
                    await bot.send_photo(user.tg_id, mailing.media_url, caption=mailing.text)
                elif mailing.media_kind is MediaKind.VIDEO and mailing.media_url:
                    await bot.send_video(user.tg_id, mailing.media_url, caption=mailing.text)
                else:
                    await bot.send_message(user.tg_id, mailing.text)

                status = SendStatus.SENT

            except TelegramRetryAfter as e:
                await asyncio.sleep(e.retry_after)
                status = SendStatus.PENDING

            except Exception:                       # noqa: BLE001
                status = SendStatus.FAILED

            async with get_session() as s:
                s.add(MailingSend(
                    mailing_id=mailing_id,
                    user_id=user.id,
                    status=status,
                ))


def send_broadcast_by_id(mailing_id: int) -> None:
    asyncio.run(_broadcast(mailing_id))
