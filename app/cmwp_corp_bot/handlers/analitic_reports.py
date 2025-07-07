from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_corp_bot.presentation.keyboards.simple_kb import analitic_reports
from app.cmwp_corp_bot.presentation.keyboards.generic_kb import build_keyboard
from app.cmwp_corp_bot.services.caption_service import render
from app.cmwp_corp_bot.db.models import Section

router = Router()


@router.callback_query(F.data == "analitic_reports")
async def show_analytics(callback: CallbackQuery):
    await callback.message.delete()
    await render(
        message=callback.message, 
        slug="analytics_menu", 
        reply_markup=analitic_reports
    )
    await callback.answer()
    

@router.callback_query(F.data == "reports")
async def open_marketbeat(callback: CallbackQuery):
    kb = await build_keyboard(Section.MARKETBEAT, add_back=True)
    await callback.message.delete()
    await render(
        message=callback.message,
        slug="marketbeat_menu",
        reply_markup=kb,
    )
    await callback.answer()


@router.callback_query(F.data == "reviews")
async def open_reviews(callback: CallbackQuery):
    kb = await build_keyboard(Section.SEGMENT, add_back=True)
    await callback.message.delete()
    await render(
        message=callback.message,
        slug="segment_menu",
        reply_markup=kb,
    )
    await callback.answer()
    

