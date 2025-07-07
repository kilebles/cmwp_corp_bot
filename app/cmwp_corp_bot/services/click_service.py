from typing import Optional
from sqlalchemy import select

from app.cmwp_corp_bot.db.repo import get_session
from app.cmwp_corp_bot.db.models import User, MenuButton, ButtonClick, Section, MediaKind


async def get_or_create_user(tg_id: int) -> User:
    async with get_session() as s:
        user = await s.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            return user
        user = User(tg_id=tg_id, full_name=f"tg_{tg_id}")
        s.add(user)
        return user


async def save_click(tg_id: int, button: MenuButton) -> None:
    async with get_session() as s:
        user = await get_or_create_user(tg_id)
        s.add(ButtonClick(user_id=user.id, button_id=button.id))
        

async def get_or_create_static_button(cb: str, label: str) -> MenuButton:
    async with get_session() as s:
        btn = await s.scalar(select(MenuButton).where(MenuButton.callback == cb))
        if btn:
            return btn
        btn = MenuButton(
            section = Section.MAIN_REPORT,
            order = 0,
            label = label,
            callback = cb,
            is_active = False,
            media_kind = MediaKind.NONE,
        )
        s.add(btn)
        await s.flush()
        return btn