from __future__ import annotations
from typing import List

from sqlalchemy import select
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from app.cmwp_corp_bot.db.models import MenuButton, Section, MediaKind
from app.cmwp_corp_bot.db.repo import get_session


async def get_active_buttons(section: Section | str) -> List[MenuButton]:
    """Возвращает активные кнопки указанного раздела, отсортированные по order."""
    if isinstance(section, Section):
        section = section.value

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

    if button.section == Section.SEGMENT:
        rows.append([
            InlineKeyboardButton(
                text="📄 Посмотреть обзоры",
                callback_data=f"segment_{button.callback}",
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
    
    
async def get_segment_detail_buttons(parent_id: int) -> list[MenuButton]:
    """Возвращает дочерние кнопки для обзоров по сегменту (SEGMENT_DETAIL)."""
    async with get_session() as session:
        result = await session.scalars(
            select(MenuButton)
            .where(
                MenuButton.section == Section.SEGMENT_DETAIL,
                MenuButton.is_active.is_(True),
                MenuButton.parent_id == parent_id
            )
            .order_by(MenuButton.order)
        )
        return list(result)