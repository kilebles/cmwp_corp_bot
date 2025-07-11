import asyncio
import logging

from app.cmwp_corp_bot.dispatcher import dp, bot

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    logger.info("Start bot")
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")