from sqlalchemy import select
from app.cmwp_corp_bot.db.models import User
from app.cmwp_corp_bot.db.repo import get_session
from app.cmwp_corp_bot.services.smtp_service import send_consult_email


async def notify_managers(tg_id: int, ctx: str) -> None:
    async with get_session() as s:
        user: User | None = await s.scalar(
            select(User).where(User.tg_id == tg_id)
        )
        if not user:
            return

        tg_link = f"tg://user?id={tg_id}"

        await send_consult_email(
            full_name=user.full_name,
            tg_link=tg_link,
            phone=user.phone or "—",
            company=user.company or "—",
            context_text=ctx,
        )