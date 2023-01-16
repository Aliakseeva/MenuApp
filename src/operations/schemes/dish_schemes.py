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
    title: str
    description: str
    price: str


class DishUpdate(BaseModel):
    title: str
    description: str
    price: str
