from __future__ import annotations
from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.cmwp_corp_bot.db.models import Section
from app.cmwp_corp_bot.services.button_service import get_active_buttons

BACK_BUTTON = InlineKeyboardButton(text="↩", callback_data="back")


async def build_keyboard(
    section: Section,
    add_back: bool = False,
) -> InlineKeyboardMarkup:
    buttons = await get_active_buttons(section)

    rows: List[List[InlineKeyboardButton]] = [
        [InlineKeyboardButton(text=b.label, callback_data=b.callback)]
        for b in buttons
    ]

    if add_back:
        rows.append([BACK_BUTTON])

    return InlineKeyboardMarkup(inline_keyboard=rows)