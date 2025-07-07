from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.cmwp_corp_bot.presentation.keyboards.simple_kb import back_kb
from app.cmwp_corp_bot.services.caption_service import render
from app.cmwp_corp_bot.services.click_service import (
    save_click,
    get_or_create_static_button,
)
from app.cmwp_corp_bot.services.consult_service import notify_managers
from app.cmwp_corp_bot.states.consult import Consult

router = Router()


@router.callback_query(F.data == 'get_consultation')
async def show_contacts(callback: CallbackQuery, state: FSMContext):
    button = await get_or_create_static_button(callback.data, "Получить консультацию")
    await save_click(callback.from_user.id, button)

    await callback.message.delete()

    await render(
        message=callback.message,
        slug="consultation",
        reply_markup=back_kb,
    )
    await state.set_state(Consult.waiting_context)
    await callback.answer()
    

@router.message(Consult.waiting_context)
async def got_context(message: Message, state: FSMContext):
    text = message.text.strip()

    await notify_managers(message.from_user.id, text)
    await render(message, slug="consult_done")
    await state.clear()