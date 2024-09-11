from sqlalchemy import Column, Integer, String, SmallInteger, Text, CHAR
from sqlalchemy.orm import  DeclarativeBase,  relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from settings import *
import uuid

class Base(DeclarativeBase):
    pass
class Bundlecode(Base):
    __tablename__ =  TABLE_PREFIX + "bundlecode"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

class Year(Base):
    __tablename__ =  TABLE_PREFIX + "year"
    id: Mapped[int] = mapped_column(primary_key=True)
    yeardate: Mapped[int] = mapped_column(SmallInteger)


class Box(Base):
    __tablename__ =  TABLE_PREFIX + "box"
    id: Mapped[int] = mapped_column(primary_key=True)
    year_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + "year" + ".id"))
    box_number: Mapped[str] = mapped_column(String(10))
    yeardate: Mapped[int] = mapped_column(SmallInteger)
    year = relationship("Year")


class Bundle(Base):
    __tablename__ = TABLE_PREFIX + "bundle"
    id: Mapped[int] = mapped_column(primary_key=True)
    box_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + "box" + ".id"))
    bundle_number: Mapped[int] = mapped_column(SmallInteger)
    code: Mapped[str] = mapped_column(String(10))
    creator: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    year_bundle: Mapped[int] = mapped_column(SmallInteger)
    yeardate: Mapped[int] = mapped_column(SmallInteger)
    box = relationship("Box")


class Item(Base):
    __tablename__ = TABLE_PREFIX + "item"
    id: Mapped[int] = mapped_column(primary_key=True)
    bundle_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + "bundle" + ".id"))
    item_number: Mapped[int] = mapped_column(SmallInteger)
    title: Mapped[str] = mapped_column(String(255))
    copy: Mapped[int] = mapped_column(SmallInteger)
    original: Mapped[int] = mapped_column(SmallInteger)
    total: Mapped[int] = mapped_column(SmallInteger)
    accesstype: Mapped[str] = mapped_column(String(2))
    yeardate: Mapped[int] = mapped_column(SmallInteger)
    codegen: Mapped[str] = mapped_column(String(20))
    cover: Mapped[str] = mapped_column(String(255))
    page_count: Mapped[str] = mapped_column(SmallInteger, nullable=True)
    filesize: Mapped[int] = mapped_column(Integer, nullable=True)
    bundle = relationship("Bundle")

