from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    submenus_count = Column(Integer)
    dishes_count = Column(Integer)

    submenus = relationship('Submenu', back_populates='menu', cascade='all, delete-orphan')


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('menus.id'))
    dishes_count = Column(Integer)

    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete-orphan')


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    price = Column(String)
    submenu_id = Column(Integer, ForeignKey('submenus.id'))

    submenu = relationship('Submenu', back_populates='dishes')
