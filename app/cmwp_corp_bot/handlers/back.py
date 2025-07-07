from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.cmwp_corp_bot.presentation.keyboards.simple_kb import main_menu_kb
from app.cmwp_corp_bot.services.caption_service import render

router = Router()


@router.callback_query(F.data == "back")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    menu_kb = await main_menu_kb()
    await callback.message.delete()
    await render(
        message=callback.message,
        slug="menu",
        reply_markup=menu_kb,
    )

    await callback.answer()
