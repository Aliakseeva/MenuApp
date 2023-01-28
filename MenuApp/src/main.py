from fastapi import FastAPI

from .database import redis_client
from .routers import dish_router, menu_router, submenu_router

app = FastAPI()
app.include_router(router=menu_router.router)
app.include_router(router=submenu_router.router)
app.include_router(router=dish_router.router)


# @app.on_event('startup')
# def startup():
#     """Database cleaning after startup"""
#
#     db = local_session()
#     db.query(Dish).delete()
#     db.query(Submenu).delete()
#     db.query(Menu).delete()
#     db.commit()
#     db.close()


@app.on_event('shutdown')
def shutdown_event():
    """Clears cache"""

    redis_client.flushdb()
