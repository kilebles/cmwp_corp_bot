from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_corp_bot.presentation.keyboards.simple_kb import back_kb

router = Router()


@router.callback_query(F.data == 'get_consultation')
async def show_contacts(callback: CallbackQuery):
    # TODO: Текст будет меняться из админки, так что его надо будет из бд подтягивать
    
    await callback.message.edit_text(
        'Задайте свой вопрос, мы обязательно ответим',
        reply_markup=back_kb
    )
    await callback.answer()