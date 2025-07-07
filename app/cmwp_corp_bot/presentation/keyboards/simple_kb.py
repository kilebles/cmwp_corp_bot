from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from app.cmwp_corp_bot.presentation.keyboards.generic_kb import BACK_BUTTON
from app.cmwp_corp_bot.services.button_service import get_active_buttons
from app.cmwp_corp_bot.db.models import Section


async def main_menu_kb() -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    buttons = await get_active_buttons(Section.MAIN_REPORT)
    if buttons:
        b = buttons[0]
        rows.append([InlineKeyboardButton(text=b.label, callback_data=b.callback)])

    rows.extend([
        [InlineKeyboardButton(text="Аналитические отчёты",
                              callback_data="analitic_reports")],
        [InlineKeyboardButton(text="Услуги компании",
                              callback_data="company_service")],
        [InlineKeyboardButton(text="Получить консультацию",
                              callback_data="get_consultation")],
        [InlineKeyboardButton(text="Мероприятия CMWP",
                              url="https://www.cmwp.ru/")],
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)


back_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='↩', callback_data='back')]
    ]
)

phone_request_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='📱 Отправить номер телефона', request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Или введите вручную в формате +7...'
)


analitic_reports = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ежеквартальный отчет MARKETBEAT', callback_data='reports')],  # TODO: будут дженерик клавы открываться на кварталы 
        [InlineKeyboardButton(text='Обзоры по сегментам рынка', callback_data='reviews')],  # TODO: будут дженерик клавы открываться на (склады, инвестиции итд)
        [InlineKeyboardButton(text='↩', callback_data='back')]
    ]
)
