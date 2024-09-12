from sqlalchemy import Column, Integer, String, SmallInteger, Text, CHAR, Date, Time, Boolean, Float
from sqlalchemy.orm import  DeclarativeBase,  relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from settings import *
import uuid
import datetime
TABLE_PREFIX = 'botui_'
class Base(DeclarativeBase):
    pass
class ReservationType(Base):
    __tablename__ =  TABLE_PREFIX + "reservationtype"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

class Multiproxy(Base):
    __tablename__ =  TABLE_PREFIX + "multiproxy"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(Text)


class Account(Base):
    __tablename__ =  TABLE_PREFIX + "account"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    api_key: Mapped[str] = mapped_column(String(255))
    token:  Mapped[str] = mapped_column(String(1000))
    payment_method_id: Mapped[int] = mapped_column(Integer)


class BotCheck(Base):
    __tablename__ =  TABLE_PREFIX + "botcheck"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255))
    startdate: Mapped[datetime.date]  = mapped_column(Date)
    enddate: Mapped[datetime.date]  = mapped_column(Date)
    seats: Mapped[int] = mapped_column(SmallInteger)
    timewanted: Mapped[datetime.time]   = mapped_column(Time())
    hoursba: Mapped[int] = mapped_column(SmallInteger)
    nonstop: Mapped[bool] = mapped_column(Boolean)
    minidle: Mapped[float]  = mapped_column(Float)
    maxidle: Mapped[float]  = mapped_column(Float)
    retrysec: Mapped[float]  = mapped_column(Float)
    sendmessage: Mapped[bool] = mapped_column(Boolean)
    account_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + "account.id"))
    account = relationship("Account")
    multiproxy_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + "multiproxy.id"))
    multiproxy = relationship("Multiproxy")
    reservation_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + "reservationtype.id"))
    reservation = relationship("ReservationType")


class BotCheckRun(Base):
    __tablename__ =  TABLE_PREFIX + "botcheckrun"
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255))
    startdate: Mapped[datetime.date]  = mapped_column(Date)
    enddate: Mapped[datetime.date]  = mapped_column(Date)
    seats: Mapped[int] = mapped_column(SmallInteger)
    timewanted: Mapped[datetime.time]   = mapped_column(Time())
    hoursba: Mapped[int] = mapped_column(SmallInteger)
    nonstop: Mapped[bool] = mapped_column(Boolean)
    minidle: Mapped[float]  = mapped_column(Float)
    maxidle: Mapped[float]  = mapped_column(Float)
    retrysec: Mapped[float]  = mapped_column(Float)
    sendmessage: Mapped[bool] = mapped_column(Boolean)
    multiproxy_name: Mapped[str] = mapped_column(String(255))
    multiproxy_value: Mapped[str] = mapped_column(String(255))
    reservation_name: Mapped[str] = mapped_column(String(255))
    account_email: Mapped[str] = mapped_column(String(255))
    account_password: Mapped[str] = mapped_column(String(255))
    account_api_key: Mapped[str] = mapped_column(String(255))
    account_token: Mapped[str] = mapped_column(String(1000))
    account_payment_method_id: Mapped[int] = mapped_column(Integer)
    pid: Mapped[int] = mapped_column(Integer)
    task: Mapped[int] = mapped_column(SmallInteger)
