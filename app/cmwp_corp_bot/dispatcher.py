from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from app.cmwp_corp_bot.settings import config
from app.cmwp_corp_bot.handlers import start
from app.cmwp_corp_bot.handlers import back

bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode='HTML')
)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(back.router)