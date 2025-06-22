from aiogram import Router, F
from aiogram.types import CallbackQuery

from cmwp_corp_bot.presentation.keyboards.simple_kb import analitic_reports

router = Router()


@router.callback_query(F.data == 'analitic_reports')
async def show_contacts(callback: CallbackQuery):
    # TODO: Текст будет меняться из админки, так что его надо будет из бд подтягивать
    
    await callback.message.edit_text(
        'Выберите действие:',
        reply_markup= analitic_reports
    )
    await callback.answer()