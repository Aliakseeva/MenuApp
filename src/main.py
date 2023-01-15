import uvicorn
from fastapi import FastAPI
# from db import *
# from models import Base
from operations.routers import menus_router as mr, submenus_router as smr, dishes_router as dr


app = FastAPI()

app.include_router(mr)
app.include_router(smr)
app.include_router(dr)

