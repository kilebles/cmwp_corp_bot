from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.cmwp_corp_bot.presentation.keyboards.simple_kb import back_kb
from app.cmwp_corp_bot.services.caption_service import render

router = Router()


@router.callback_query(F.data == 'get_consultation')
async def show_contacts(callback: CallbackQuery):    
    await render(message=callback.message, slug='Консультация', reply_markup=back_kb)
    await callback.answer()