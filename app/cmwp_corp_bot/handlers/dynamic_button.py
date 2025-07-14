from aiogram import Router
from aiogram.types import CallbackQuery
from contextlib import suppress
from aiogram.fsm.context import FSMContext

from app.cmwp_corp_bot.services.button_service import (
    get_button_by_callback,
)
from app.cmwp_corp_bot.services.button_service import show_button_detail, get_segment_detail_buttons
from app.cmwp_corp_bot.presentation.keyboards.simple_kb import back_kb
from app.cmwp_corp_bot.services.click_service import save_click
from app.cmwp_corp_bot.states.consult import Consult
from app.cmwp_corp_bot.services.caption_service import render
from app.cmwp_corp_bot.db.models import Section

router = Router()


@router.callback_query(lambda c: c.data.startswith("segment_"))
async def show_segment_detail(callback: CallbackQuery):
    orig_cb = callback.data.removeprefix("segment_")
    parent_button = await get_button_by_callback(orig_cb)
    if not parent_button:
        await callback.answer("Обзор не найден", show_alert=True)
        return

    children = await get_segment_detail_buttons(orig_cb)

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from app.cmwp_corp_bot.presentation.keyboards.generic_kb import BACK_BUTTON

    if not children:
        await callback.answer("Нет обзоров", show_alert=True)
        return

    rows = [
        [InlineKeyboardButton(text=child.label, url=child.link_url)]
        for child in children
    ]
    rows.append([BACK_BUTTON])

    kb = InlineKeyboardMarkup(inline_keyboard=rows)

    with suppress(Exception):
        await callback.message.delete()

    await callback.message.answer(f"<b>{parent_button.label}</b>", reply_markup=kb, parse_mode="HTML")
    await callback.answer()


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

    if button.section == Section.SEGMENT:
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        from app.cmwp_corp_bot.presentation.keyboards.generic_kb import BACK_BUTTON
        from app.cmwp_corp_bot.services.button_service import get_segment_detail_buttons

        children = await get_segment_detail_buttons(button.id)  # <-- вот тут заменили

        if not children:
            await callback.message.answer("Нет обзоров", reply_markup=InlineKeyboardMarkup(inline_keyboard=[[BACK_BUTTON]]))
            await callback.answer("Нет обзоров", show_alert=True)
            return

        rows = [
            [InlineKeyboardButton(text=child.label, url=child.link_url)]
            for child in children
        ]
        rows.append([BACK_BUTTON])

        kb = InlineKeyboardMarkup(inline_keyboard=rows)
        await callback.message.answer(f"<b>{button.label}</b>", reply_markup=kb, parse_mode="HTML")
        await callback.answer()
        return

    await show_button_detail(callback.message, button)
    await callback.answer()