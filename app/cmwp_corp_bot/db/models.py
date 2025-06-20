import enum, datetime as dt
from sqlalchemy import BigInteger, Boolean, Enum, ForeignKey, JSON, Text, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.cmwp_corp_bot.db.session import Base
