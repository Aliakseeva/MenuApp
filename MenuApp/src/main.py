from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from MenuApp.info import description, title, version

from .routers import dish_router, menu_router, submenu_router, task_router

app = FastAPI(
    docs_url="/",
    swagger_ui_parameters={"syntaxHighlight.theme": "nord"},
)

app.include_router(router=menu_router.router)
app.include_router(router=submenu_router.router)
app.include_router(router=dish_router.router)
app.include_router(router=task_router.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=title,
        version=version,
        description=description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
