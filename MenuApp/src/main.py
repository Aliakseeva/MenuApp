from fastapi import FastAPI

from .database import local_session
from .models import Menu, Submenu, Dish
from .routers import menu_router, submenu_router, dish_router


app = FastAPI()
app.include_router(router=menu_router.router)
app.include_router(router=submenu_router.router)
app.include_router(router=dish_router.router)


@app.on_event('startup')
def startup():
    """Database cleaning after startup"""

    db = local_session()
    db.query(Dish).delete()
    db.query(Submenu).delete()
    db.query(Menu).delete()
    db.commit()
    db.close()


@app.get('/', response_model=None)
def say_hello():
    """Hello-page"""
    return {'Hello': 'there'}
