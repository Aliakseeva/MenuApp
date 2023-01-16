from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


metadata = MetaData()


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)

    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete-orphan')


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    dishes_count = Column(Integer, default=0)

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete-orphan')


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(String, default='0.00')
    submenu_id = Column(Integer, ForeignKey('submenus.id'))

    submenu = relationship('Submenu', back_populates='dishes')
