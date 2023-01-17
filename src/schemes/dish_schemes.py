from pydantic import BaseModel


class Dish(BaseModel):
    id: str
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishCreateUpdate(BaseModel):
    title: str
    description: str