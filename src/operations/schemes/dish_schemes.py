from pydantic import BaseModel


class Dish(BaseModel):
    id: str
    submenu_id: str
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishCreate(BaseModel):
    submenu_id: str
    title: str
    description: str
    price: str


class DishUpdate(BaseModel):
    submenu_id: str
    title: str
    description: str
    price: str
