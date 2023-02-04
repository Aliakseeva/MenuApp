from pydantic import BaseModel


class Dish(BaseModel):
    id: str
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "31416",
                "title": "Chop",
                "description": "Is a dish",
                "price": "9.99",
            },
        }


class DishCreateUpdate(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Chop",
                "description": "Is a dish",
                "price": "9.99",
            },
        }
