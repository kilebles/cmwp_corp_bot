import enum
import datetime as dt
import uuid
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.cmwp_corp_bot.db.session import Base


class Section(str, enum.Enum):
    MAIN_REPORT = "mainreport"
    MARKETBEAT = "marketbeat"
    SEGMENT = "segment"
    ANALYTICS = "analytics"


class MediaKind(str, enum.Enum):
    NONE = "none"
    PHOTO = "photo"
    VIDEO = "video"


class SendStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Content(Base):
    __tablename__ = "contents"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(Text, unique=True)
    text: Mapped[str] = mapped_column(Text)
    media_kind: Mapped[MediaKind] = mapped_column(Enum(MediaKind, name="mediakind"), default=MediaKind.NONE)
    media_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    buttons: Mapped[list["MenuButton"]] = relationship("MenuButton", back_populates="content", cascade="all,delete")


class MenuButton(Base):
    __tablename__ = "menu_buttons"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    section: Mapped[Section] = mapped_column(Enum(Section, name="section"), default=Section.MARKETBEAT)
    order: Mapped[int] = mapped_column(Integer, default=0)
    label: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    media_kind: Mapped[MediaKind] = mapped_column(Enum(MediaKind, name="mediakind"), default=MediaKind.NONE)
    media_url: Mapped[str | None] = mapped_column(Text)
    link_url: Mapped[str | None] = mapped_column(Text)
    callback: Mapped[str] = mapped_column(Text, unique=True, default=lambda: str(uuid.uuid4()))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    content_id: Mapped[int | None] = mapped_column(ForeignKey("contents.id"))

    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    content: Mapped["Content"] = relationship("Content", back_populates="buttons")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str | None] = mapped_column(Text)
    position: Mapped[str | None] = mapped_column(Text)
    email: Mapped[str | None] = mapped_column(Text)
    phone: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    clicks: Mapped[list["ButtonClick"]] = relationship(
        "ButtonClick", back_populates="user", cascade="all,delete"
    )
    mailings: Mapped[list["MailingSend"]] = relationship(
        "MailingSend", back_populates="user", cascade="all,delete"
    )


class ButtonClick(Base):
    __tablename__ = "button_clicks"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    button_id: Mapped[int] = mapped_column(ForeignKey("menu_buttons.id"), nullable=False)
    ts: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="clicks")
    button: Mapped["MenuButton"] = relationship("MenuButton")


class Mailing(Base):
    __tablename__ = "mailings"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text)
    media_kind: Mapped[MediaKind] = mapped_column(Enum(MediaKind, name="mediakind"), default=MediaKind.NONE)
    media_url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sends: Mapped[list["MailingSend"]] = relationship("MailingSend", back_populates="mailing", cascade="all,delete")


class MailingSend(Base):
    __tablename__ = "mailing_sends"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mailing_id: Mapped[int] = mapped_column(ForeignKey("mailings.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[SendStatus] = mapped_column(Enum(SendStatus, name="sendstatus"), default=SendStatus.PENDING)
    ts: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    mailing: Mapped["Mailing"] = relationship("Mailing", back_populates="sends")
    user: Mapped["User"] = relationship("User", back_populates="mailings")
