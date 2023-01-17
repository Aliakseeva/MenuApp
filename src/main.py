from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import local_session, get_db
from .models import Menu, Submenu, Dish
from .schemes import menu_schemes as m, submenu_schemes as sm, dish_schemes as d
from .crud import delete, read, create, update

app = FastAPI()


@app.on_event('startup')
def startup():
    """Database cleaning after startup"""

    db = local_session()
    db.query(Menu).delete()
    db.query(Submenu).delete()
    db.query(Dish).delete()
    db.commit()
    db.close()


# @app.on_event('shutdown')
# def shutdown():
#     db = local_session()
#     db.query(Menu).delete()
#     db.query(Submenu).delete()
#     db.query(Dish).delete()
#     db.commit()
#     db.close()


@app.get('/api/v1/menus', response_model=List[m.Menu])
def get_all_menus(db: Session = Depends(get_db)):
    """Gets a list of menu"""

    menus_l = read.get_menus(db=db)
    return menus_l


@app.get('/api/v1/menus/{menu_id}', response_model=m.Menu)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """Gets certain menu by id"""

    menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if menu:
        return menu
    else:
        raise HTTPException(status_code=404, detail='menu not found')


@app.post('/api/v1/menus', response_model=m.Menu)
def create_menu(menu: m.MenuCreateUpdate, db: Session = Depends(get_db)):
    """Creates a new menu"""

    new_menu = create.create_menu(db=db, menu=menu)
    return new_menu


@app.patch('/api/v1/menus/{menu_id}', response_model=m.Menu)
def update_menu(menu_id: int, menu: m.MenuCreateUpdate, db: Session = Depends(get_db)):
    """Updates the menu"""

    upd_menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if not upd_menu:
        raise HTTPException(status_code=404, detail='menu not found')
    else:
        upd_menu.title = menu.title
        upd_menu.description = menu.description
        return update.update_menu(db=db, menu_id=menu_id)


@app.delete('/api/v1/menus/{menu_id}', response_model=None)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Deletes the menu"""

    del_menu = delete.delete_menu(db=db, menu_id=menu_id)
    if del_menu:
        return {'status': True, 'message': 'The menu has been deleted'}

#####################################################################


@app.post('/api/v1/menus/{menu_id}/submenus', response_model=sm.Submenu)
def create_submenu(menu_id: int, submenu: sm.SubmenuCreateUpdate, db: Session = Depends(get_db)):
    """Creates a new submenu"""

    new_submenu = create.create_submenu(db=db, submenu=submenu, menu_id=menu_id)
    return new_submenu


@app.get('/api/v1/menus/{menu_id}/submenus', response_model=List[sm.Submenu])
def read_all_submenus(menu_id: int, db: Session = Depends(get_db)):
    """Gets a list of submenus"""

    submenus_l = read.get_submenus(db=db, menu_id=menu_id)
    return submenus_l


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=sm.Submenu)
def read_submenu(submenu_id: int, db: Session = Depends(get_db)):
    """Gets the submenu"""

    submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if submenu:
        return submenu
    else:
        raise HTTPException(status_code=404, detail='submenu not found')


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=sm.Submenu)
def update_submenu(submenu_id: int, submenu: sm.SubmenuCreateUpdate, db: Session = Depends(get_db)):
    """Updates the submenu"""

    upd_submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if not upd_submenu:
        raise HTTPException(status_code=404, detail='submenu not found')
    else:
        upd_submenu.title = submenu.title
        upd_submenu.description = submenu.description
        return update.update_submenu(db=db, submenu_id=submenu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=sm.Submenu)
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Deletes the submenu """

    del_submenu = delete.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if del_submenu:
        return {'status': True, 'message': 'The menu has been deleted'}


########################################

@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=d.Dish)
def create_dish(menu_id: int, submenu_id: int, dish: d.DishCreateUpdate, db: Session = Depends(get_db)):
    """Creating a new dish"""

    return create.create_dish(db=db, dish=dish, menu_id=menu_id, submenu_id=submenu_id)


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', response_model=List[d.Dish])
def get_all_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Gets a list of menus"""

    dishes_l = read.get_dishes(db=db, submenu_id=submenu_id)
    return dishes_l


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=d.Dish)
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Gets certain dish by id"""

    dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    if dish:
        return dish
    else:
        raise HTTPException(status_code=404, detail='dish not found')


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}', response_model=d.Dish)
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: d.DishCreateUpdate, db: Session = Depends(get_db)):
    """Updating certain dish by id"""

    upd_dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    if not upd_dish:
        raise HTTPException(status_code=404, detail='dish not found')
    else:
        upd_dish.title = dish.title
        upd_dish.description = dish.description
        upd_dish.price = dish.price
        return update.update_dish(db=db, dish_id=dish_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', response_model=d.Dish)
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Deletes the dish by id"""

    del_dish = delete.delete_dish(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)
    if del_dish:
        return {'status': True, 'message': 'The dish has been deleted'}



# TODO
# при выводе блюда убрать из полей submenu id
# dish price to float
# edit pep
# добавить httpexeptions

