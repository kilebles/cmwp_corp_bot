from __future__ import annotations

from typing import Any, Optional, Tuple

from aiogram.types import Message
from sqlalchemy import select

from app.cmwp_corp_bot.db.repo import get_session
from app.cmwp_corp_bot.db.models import Content, MediaKind


async def get_content(slug: str, **fmt: Any) -> Optional[Tuple[Content, str]]:
    async with get_session() as session:
        content: Content | None = await session.scalar(
            select(Content).where(Content.slug == slug)
        )
        if not content:
            return None

        text = content.text.format(**fmt) if fmt else content.text
        return content, text


async def render(
    message: Message,
    slug: str,
    reply_markup=None,
    **fmt: Any,
):
    result = await get_content(slug, **fmt)
    if not result:
        return await message.answer(
            f'❗️ Описание с ключом "{slug}" ещё не добавлено в админ-панели.',
            reply_markup=reply_markup,
        )

    content, text = result
    file_or_url = content.media_url

    if content.media_kind == MediaKind.PHOTO and file_or_url:
        return await message.answer_photo(file_or_url, caption=text, reply_markup=reply_markup)

    if content.media_kind == MediaKind.VIDEO and file_or_url:
        return await message.answer_video(file_or_url, caption=text, reply_markup=reply_markup)

    return await message.answer(text, reply_markup=reply_markup)
