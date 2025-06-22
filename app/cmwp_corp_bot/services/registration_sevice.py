import re
import asyncio
from contextlib import suppress
from aiogram.types import Message, ReplyKeyboardRemove

from app.cmwp_corp_bot.presentation.keyboards.simple_kb import phone_request_kb, main_menu_kb



def is_russian(text: str) -> bool:
    return bool(re.fullmatch(r'[А-Яа-яЁё\- ]{2,50}', text.strip()))


def is_valid_email(text: str) -> bool:
    return bool(re.fullmatch(r'[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+', text.strip()))


def normalize_phone(text: str) -> str:
    digits = re.sub(r'\D', '', text)
    if digits.startswith('8'):
        digits = '7' + digits[1:]
    elif digits.startswith('9') and len(digits) == 10:
        digits = '7' + digits
    elif digits.startswith('7'):
        pass
    else:
        return ''
    return f'+{digits}'


def is_valid_phone(text: str) -> bool:
    return bool(re.fullmatch(r'^\+7\d{10}$', normalize_phone(text)))


async def send_temp_warning(message: Message, text: str, delay: float = 3.0):
    warn = await message.answer(text)
    async def auto_delete():
        await asyncio.sleep(delay)
        with suppress(Exception):
            await warn.delete()
    asyncio.create_task(auto_delete())


async def registration_dialog(message: Message):
    # TODO: Добавлять зарегистрированные данные в БД
    
    await message.answer('Введите ФИО:')
    while True:
        msg: Message = yield
        if is_russian(msg.text):
            full_name = msg.text.strip()
            break
        await send_temp_warning(msg, '❌ Введите корректное ФИО (только кириллица)')

    await message.answer('Введите название компании:')
    msg: Message = yield
    company = msg.text.strip()

    await message.answer('Введите вашу должность:')
    msg: Message = yield
    position = msg.text.strip()

    await message.answer('Введите номер телефона:', reply_markup=phone_request_kb)
    while True:
        msg: Message = yield
        phone_raw = msg.contact.phone_number if msg.contact else msg.text
        if phone_raw and is_valid_phone(phone_raw):
            phone = normalize_phone(phone_raw)
            break
        await send_temp_warning(msg, '❌ Номер должен быть в формате +7XXXXXXXXXX')
        
    await message.answer('Введите email:', reply_markup=ReplyKeyboardRemove())
    while True:
        msg: Message = yield
        if is_valid_email(msg.text):
            email = msg.text.strip()
            break
        await send_temp_warning(msg, '❌ Введите корректный email')
        
    result = (
        f"Вы успешно авторизовались!\n"
        f"👤 ФИО: {full_name}\n"
        f"🏢 Компания: {company}\n"
        f"💼 Должность: {position}\n"
        f"📧 Email: {email}\n"
        f"📱 Телефон: {phone}"
    )
    await message.answer(result, reply_markup=main_menu_kb)
    
