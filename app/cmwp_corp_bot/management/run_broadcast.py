import sys
import asyncio

from app.cmwp_corp_bot.services.broadcast_service_inner import _broadcast


if __name__ == "__main__":
    mailing_id = int(sys.argv[1])
    asyncio.run(_broadcast(mailing_id))
