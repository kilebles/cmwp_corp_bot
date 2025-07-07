from __future__ import annotations

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_corp_bot.presentation.keyboards.generic_kb import build_keyboard
from app.cmwp_corp_bot.presentation.keyboards.simple_kb import back_kb
from app.cmwp_corp_bot.services.caption_service import render
from app.cmwp_corp_bot.db.models import Section

router = Router()


@router.callback_query(F.data == "company_service")
async def open_company_services(callback: CallbackQuery) -> None:
    kb = await build_keyboard(Section.ANALYTICS, add_back=True)

    await callback.message.delete()

    await render(
        message=callback.message,
        slug="company_service_menu",
        reply_markup=kb,
    )
    await callback.answer()
