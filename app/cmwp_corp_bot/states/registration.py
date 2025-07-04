from __future__ import annotations
import re
from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    full_name = State()
    company = State()
    position = State()
    phone = State()
    email = State()


def is_russian(text: str) -> bool:
    return bool(re.fullmatch(r"[А-Яа-яЁё\- ]{2,50}", text.strip()))


def is_valid_email(text: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+", text.strip()))


def normalize_phone(text: str) -> str:
    digits = re.sub(r"\D", "", text)
    if digits.startswith("8"):
        digits = "7" + digits[1:]
    elif digits.startswith("9") and len(digits) == 10:
        digits = "7" + digits
    elif not digits.startswith("7"):
        return ""
    return f"+{digits}"


def is_valid_phone(text: str) -> bool:
    return bool(re.fullmatch(r"^\+7\d{10}$", normalize_phone(text)))
