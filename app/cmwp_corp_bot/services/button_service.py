from __future__ import annotations
from typing import List

from sqlalchemy import select
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.cmwp_corp_bot.db.models import MenuButton, Section, MediaKind
from app.cmwp_corp_bot.db.repo import get_session


async def get_active_buttons(section: Section) -> List[MenuButton]:
    """Возвращает активные кнопки указанного раздела, отсортированные по order."""
    async with get_session() as session:
        result = await session.scalars(
            select(MenuButton)
            .where(
                MenuButton.section == section,
                MenuButton.is_active.is_(True),
            )
            .order_by(MenuButton.order)
        )
        return list(result)
    

async def get_button(callback_data: str) -> Optional[MenuButton]:
    """Возвращает кнопку по callback-data или None."""
    async with get_session() as s:
        return await s.scalar(
            select(MenuButton).where(MenuButton.callback == callback_data,
                                     MenuButton.is_active.is_(True))
        )
    
    
async def get_button_by_callback(cb: str) -> MenuButton | None:
    async with get_session() as s:
        return await s.scalar(
            select(MenuButton).where(MenuButton.callback == cb,
                                     MenuButton.is_active.is_(True))
        )


def detail_keyboard(button: MenuButton) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    if button.section == Section.MARKETBEAT and button.link_url:
        rows.append([
            InlineKeyboardButton(
                text="📄 Посмотреть отчёт",
                url=button.link_url,
            )
        ])

    if button.section == Section.SEGMENT and button.link_url:
        rows.append([
            InlineKeyboardButton(
                text="📄 Посмотреть обзор",
                url=button.link_url,
            )
        ])

    if button.section == Section.ANALYTICS:
        rows.append([
            InlineKeyboardButton(
                text="💬 Получить консультацию",
                callback_data=f"consult_{button.callback}",
            )
        ])

    from app.cmwp_corp_bot.presentation.keyboards.generic_kb import BACK_BUTTON
    rows.append([BACK_BUTTON])

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def show_button_detail(message: Message, button: MenuButton):
    text = button.description or " "

    if button.media_kind == MediaKind.PHOTO and button.media_url:
        await message.answer_photo(button.media_url, caption=text,
                                   reply_markup=detail_keyboard(button))
        return
    if button.media_kind == MediaKind.VIDEO and button.media_url:
        await message.answer_video(button.media_url, caption=text,
                                   reply_markup=detail_keyboard(button))
        return

    await message.answer(text, reply_markup=detail_keyboard(button),
                         parse_mode="HTML")