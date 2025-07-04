from __future__ import annotations

import asyncio
from contextlib import suppress
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app.cmwp_corp_bot.presentation.keyboards.simple_kb import phone_request_kb, main_menu_kb
from app.cmwp_corp_bot.states.registration import (
    Registration,
    is_russian,
    is_valid_email,
    is_valid_phone,
    normalize_phone,
)
from app.cmwp_corp_bot.services.registration_service import save_registration, user_exists
from app.cmwp_corp_bot.services.caption_service import render

router = Router()


async def temp_warn(msg: Message, text: str, delay: float = 3) -> None:
    warn = await msg.answer(text)
    async def _auto_del() -> None:
        await asyncio.sleep(delay)
        with suppress(Exception):
            await warn.delete()
    asyncio.create_task(_auto_del())


@router.message(CommandStart())
async def start_registration(message: Message, state: FSMContext) -> None:
    await state.clear()

    if await user_exists(message.from_user.id):
        await render(message, slug='меню', reply_markup=main_menu_kb)
        return

    await message.render(message, slug='Регистрация')
    await state.set_state(Registration.full_name)


@router.message(Registration.full_name)
async def reg_full_name(msg: Message, state: FSMContext) -> None:
    if not is_russian(msg.text):
        await temp_warn(msg, "❌ Введите корректное ФИО (только кириллица)")
        return
    await state.update_data(full_name=msg.text.strip())
    await msg.answer("Введите название компании:")
    await state.set_state(Registration.company)


@router.message(Registration.company)
async def reg_company(msg: Message, state: FSMContext) -> None:
    await state.update_data(company=msg.text.strip())
    await msg.answer("Введите вашу должность:")
    await state.set_state(Registration.position)


@router.message(Registration.position)
async def reg_position(msg: Message, state: FSMContext) -> None:
    await state.update_data(position=msg.text.strip())
    await msg.answer("Введите номер телефона:", reply_markup=phone_request_kb)
    await state.set_state(Registration.phone)


@router.message(Registration.phone, F.contact)
@router.message(Registration.phone, F.text)
async def reg_phone(msg: Message, state: FSMContext) -> None:
    raw = msg.contact.phone_number if msg.contact else msg.text
    phone = normalize_phone(raw or "")
    if not is_valid_phone(phone):
        await temp_warn(msg, "❌ Номер должен быть в формате +7XXXXXXXXXX")
        return
    await state.update_data(phone=phone)
    await msg.answer("Введите email:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Registration.email)


@router.message(Registration.email)
async def reg_email(msg: Message, state: FSMContext) -> None:
    if not is_valid_email(msg.text):
        await temp_warn(msg, "❌ Введите корректный email")
        return

    await state.update_data(email=msg.text.strip())
    data = await state.get_data()

    await save_registration(
        {
            "tg_user": msg.from_user,
            "full_name": data["full_name"],
            "company": data["company"],
            "position": data["position"],
            "phone": data["phone"],
            "email": data["email"],
        }
    )

    reply = (
        "Вы успешно зарегистрированы!\n\n"
        f"👤 ФИО: {data['full_name']}\n"
        f"🏢 Компания: {data['company']}\n"
        f"💼 Должность: {data['position']}\n"
        f"📧 Email: {data['email']}\n"
        f"📱 Телефон: {data['phone']}"
    )

    await msg.answer(reply, reply_markup=main_menu_kb)
    await state.clear()