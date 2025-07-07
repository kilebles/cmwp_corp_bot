from aiogram import Router
from aiogram.types import CallbackQuery
from contextlib import suppress
from aiogram.fsm.context import FSMContext

from app.cmwp_corp_bot.services.button_service import (
    get_button_by_callback,
)
from app.cmwp_corp_bot.services.button_service import show_button_detail
from app.cmwp_corp_bot.presentation.keyboards.simple_kb import back_kb
from app.cmwp_corp_bot.services.click_service import save_click
from app.cmwp_corp_bot.states.consult import Consult
from app.cmwp_corp_bot.services.caption_service import render

router = Router()




@router.callback_query(lambda c: c.data.startswith("consult_"))
async def consult(callback: CallbackQuery, state: FSMContext):
    orig_cb = callback.data.removeprefix("consult_")
    button = await get_button_by_callback(orig_cb)
    if not button:
        await callback.answer("Нет шаблона консультации", show_alert=True)
        return

    await save_click(callback.from_user.id, button)

    with suppress(Exception):
        await callback.message.delete()

    await render(
        message=callback.message,
        slug="consultation",
        reply_markup=back_kb,
    )
    await state.set_state(Consult.waiting_context)
    await callback.answer()


@router.callback_query()
async def dynamic_button(callback: CallbackQuery):
    button = await get_button_by_callback(callback.data)
    if not button:
        return

    await save_click(callback.from_user.id, button)
    
    with suppress(Exception):
        await callback.message.delete()

    await show_button_detail(callback.message, button)
    await callback.answer()
