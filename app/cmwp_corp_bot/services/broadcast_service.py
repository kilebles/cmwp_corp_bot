import asyncio
from sqlalchemy import select
from app.cmwp_corp_bot.db.repo import get_session
from app.cmwp_corp_bot.db.models import User, Mailing, MailingSend, SendStatus, MediaKind
from app.cmwp_corp_bot.dispatcher import bot


async def _broadcast_message(mailing_id: int):
    async with get_session() as session:
        mailing = await session.get(Mailing, mailing_id)
        if not mailing:
            return

        users = await session.scalars(select(User))
        users = list(users)

        for user in users:
            try:
                if mailing.media_kind == MediaKind.PHOTO and mailing.media_url:
                    await bot.send_photo(user.tg_id, photo=mailing.media_url, caption=mailing.text)
                elif mailing.media_kind == MediaKind.VIDEO and mailing.media_url:
                    await bot.send_video(user.tg_id, video=mailing.media_url, caption=mailing.text)
                else:
                    await bot.send_message(user.tg_id, text=mailing.text)

                status = SendStatus.SENT
            except Exception:
                status = SendStatus.FAILED

            session.add(MailingSend(
                mailing_id=mailing.id,
                user_id=user.id,
                status=status,
            ))

        await session.commit()


def send_broadcast_by_id(mailing_id: int):
    asyncio.run(_broadcast_message(mailing_id))
