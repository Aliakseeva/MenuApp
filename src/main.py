from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import local_session, get_db
from .models import Menu, Submenu, Dish
from .operations.schemes import menu_schemes as m, submenu_schemes as sm, dish_schemes as d
from .operations.crud import create
from .operations.crud import read
from .operations.crud import update
from .operations.crud import delete


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


@app.get('/api/v1/menus', status_code=200)
def get_all_menus(db: Session = Depends(get_db)):
    """Gets a list of menu"""

    menus_l = read.get_menus(db=db)
    return menus_l


@app.get('/api/v1/menus/{menu_id}')
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """Gets certain menu by id"""

    menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    return menu if menu else {'detail': 'menu not found'}


@app.post('/api/v1/menus')
def create_menu(menu: m.MenuCreate, db: Session = Depends(get_db)):
    """Creates a new menu"""

    new_menu = create.create_menu(db=db, menu=menu)
    return new_menu


@app.patch('/api/v1/menus/{menu_id}')
def update_menu(menu_id: int, menu: m.MenuUpdate, db: Session = Depends(get_db)):
    """Updates the menu"""

    upd_menu = read.get_menu_by_id(db=db, menu_id=menu_id)
    if not upd_menu:
        return {'detail': 'menu not found'}
    else:
        upd_menu.title = menu.title
        upd_menu.description = menu.description
        return update.update_menu(db=db, menu_id=menu_id)


@app.delete('/api/v1/menus/{menu_id}')
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Deletes the menu"""

    del_menu = delete.delete_menu(db=db, menu_id=menu_id)
    if del_menu:
        return {'status': True, 'message': 'The menu has been deleted'}

#####################################################################


@app.post('/api/v1/menus/{menu_id}/submenus')
def create_submenu(menu_id: int, submenu: sm.SubmenuCreate, db: Session = Depends(get_db)):
    """Creates a new submenu"""

    new_submenu = create.create_submenu(db=db, submenu=submenu, menu_id=menu_id)
    return new_submenu


@app.get('/api/v1/menus/{menu_id}/submenus')
def read_all_submenus(menu_id: int, db: Session = Depends(get_db)):
    """Gets a list of submenus"""

    submenus_l = read.get_submenus(db=db, menu_id=menu_id)
    return submenus_l


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def read_submenu(submenu_id: int, db: Session = Depends(get_db)):
    """Gets the submenu"""

    submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    return submenu if submenu else {'detail': 'submenu not found'}


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def update_submenu(submenu_id: int, submenu: sm.SubmenuUpdate, db: Session = Depends(get_db)):
    """Updates the submenu"""

    upd_submenu = read.get_submenu_by_id(db=db, submenu_id=submenu_id)
    if not upd_submenu:
        return {'detail': 'submenu not found'}
    else:
        upd_submenu.title = submenu.title
        upd_submenu.description = submenu.description
        return update.update_submenu(db=db, submenu_id=submenu_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def delete_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """ """

    del_submenu = delete.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if del_submenu:
        return {'status': True, 'message': 'The menu has been deleted'}


########################################

@app.post('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def create_dish(menu_id: int, submenu_id: int, dish: d.DishCreate, db: Session = Depends(get_db)):
    """Creating a new dish"""

    return create.create_dish(db=db, dish=dish, menu_id=menu_id, submenu_id=submenu_id)



@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
def get_all_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    """Gets a list of menus"""

    dishes_l = read.get_dishes(db=db, submenu_id=submenu_id)
    return dishes_l


@app.get('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Gets certain dish by id"""

    dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    return dish if dish else {'detail': 'dish not found'}


@app.patch('/api/v1/menus/{menu_id}/submenus/{submenu_id}')
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: d.DishUpdate, db: Session = Depends(get_db)):
    """Updating certain dish by id"""

    upd_dish = read.get_dish_by_id(db=db, dish_id=dish_id)
    if not upd_dish:
        return {'detail': 'dish not found'}
    else:
        upd_dish.title = dish.title
        upd_dish.description = dish.description
        upd_dish.price = dish.price
        return update.update_dish(db=db, dish_id=dish_id)


@app.delete('/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    """Deletes the dish by id"""

    del_dish = delete.delete_dish(db=db, dish_id=dish_id, menu_id=menu_id, submenu_id=submenu_id)
    if del_dish:
        return {'status': True, 'message': 'The dish has been deleted'}



# TODO
# при выводе блюда убрать из полей submenu id
# dish price to float
# edit pep

