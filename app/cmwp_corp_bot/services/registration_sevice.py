import re
import asyncio

from contextlib import suppress

from aiogram.types import Message, ReplyKeyboardRemove


def is_russian(text: str) -> bool:
    return bool(re.fullmatch(r'[А-Яа-яЁё\- ]{2,50}', text.strip()))


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
    phone = normalize_phone(text)
    return bool(re.fullmatch(r'^\+7\d{10}$', phone))


async def send_temp_warning(message: Message, text: str, delay: float = 3.0):
    """Автоудаление предупреждения"""
    warn = await message.answer(text)

    async def auto_delete():
        await asyncio.sleep(delay)
        with suppress(Exception):
            await warn.delete()

    asyncio.create_task(auto_delete())
