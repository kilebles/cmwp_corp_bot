from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from app.cmwp_corp_bot.settings import config
from app.cmwp_corp_bot.handlers import start
from app.cmwp_corp_bot.handlers import back
from app.cmwp_corp_bot.handlers import get_consultation
from app.cmwp_corp_bot.handlers import analitic_reports
from app.cmwp_corp_bot.handlers import dynamic_button
from app.cmwp_corp_bot.handlers import company_service

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(back.router)
dp.include_router(get_consultation.router)
dp.include_router(analitic_reports.router)
dp.include_router(company_service.router)
dp.include_router(dynamic_button.router)