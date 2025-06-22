from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Скачать отчет X', callback_data='install_report')],  # TODO: Эта кнопка пойдет в БД для ее изменения из админки
        [InlineKeyboardButton(text='Аналитические отчеты', callback_data='analitic_reports')],
        [InlineKeyboardButton(text='Услуги комапнии', callback_data='company_service')],
        [InlineKeyboardButton(text='Получить консультацию', callback_data='get_consultation')],
        [InlineKeyboardButton(text='Мероприятия CMWP', url='https://www.cmwp.ru/')]
    ]
)

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
