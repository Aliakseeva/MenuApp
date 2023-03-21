from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, func, select
from sqlalchemy.orm import MapperProperty, column_property, relationship

from .database import Base

metadata = MetaData()


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(String, default="0.00")
    submenu_id = Column(Integer, ForeignKey("submenus.id", ondelete="CASCADE"))

    submenu = relationship("Submenu", back_populates="dishes")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"))

    dishes_count: MapperProperty = column_property(
        select(func.count(Dish.id))
        .where(Dish.submenu_id == id)
        .correlate_except(Dish)
        .scalar_subquery(),
    )

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)

    submenus_count: MapperProperty = column_property(
        select(func.count(Submenu.id))
        .where(Submenu.menu_id == id)
        .correlate_except(Submenu)
        .scalar_subquery(),
    )
    dishes_count: MapperProperty = column_property(
        select(func.count(Dish.id))
        .join(Submenu, Submenu.menu_id == id)
        .where(Dish.submenu_id == Submenu.id)
        .correlate_except(Submenu)
        .scalar_subquery(),
    )

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")
