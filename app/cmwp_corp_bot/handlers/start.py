from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from typing import AsyncGenerator

from app.cmwp_corp_bot.services.registration_sevice import registration_dialog


router = Router()

active_dialogs: dict[int, AsyncGenerator] = {}


@router.message(CommandStart())
async def cmd_start(message: Message):
    #TODO: Текст будет из админки, так что message_answer из бд будем подтягивать
    
    await message.answer('👋 Добро пожаловать! Давайте начнём регистрацию.')

    dialog = registration_dialog(message)
    active_dialogs[message.from_user.id] = dialog
    await dialog.asend(None)


@router.message()
async def dialog_step(message: Message):
    dialog = active_dialogs.get(message.from_user.id)
    if not dialog:
        return

    try:
        await dialog.asend(message)
    except StopAsyncIteration:
        del active_dialogs[message.from_user.id]
