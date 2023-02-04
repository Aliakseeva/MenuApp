from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .database import redis_client
from .routers import dish_router, menu_router, submenu_router

app = FastAPI(
    docs_url="/",
    swagger_ui_parameters={"syntaxHighlight.theme": "nord"},
)
app.include_router(router=menu_router.router)
app.include_router(router=submenu_router.router)
app.include_router(router=dish_router.router)

# TODO: удалить лишние куски кода (в комментариях)


@app.on_event("shutdown")
def shutdown_event():
    """Clear cache before shutdown"""
    redis_client.flushdb()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MenuApp",
        version="beta",
        description="This is a simple Restaurant Menu Server "
        "based on the OpenAPI 3.0 specification.\n"
        "The project is based on next services:\n\n"
        "🐍 Python3\n\n"
        "⚡ FastAPI Web framework\n\n"
        "🐘 PostgreSQL database\n\n"
        "⏳ Redis-cache\n\n"
        "📜 SQLAlchemy ORM\n\n"
        "📝 Alembic database migration tool\n\n"
        "🦄 Uvicorn ASGI web server\n\n"
        "🐳 Docker containers\n\n"
        "✅ Pytest\n\n"
        "_Some useful links:_\n\n"
        "- [GitHub repository](https://github.com/Aliakseeva/MenuApp)",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
