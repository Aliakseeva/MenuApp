from pydantic import BaseModel



class Menu(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "0921",
                "title": "Breakfast",
                "description": "Breakfast menu description",
                "submenus_count": 2,
                "dishes_count": 9,
            },
        }


class MenuCreateUpdate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Lunch menu",
                "description": "Lunch menu description",
            },
        }

class BaseSchema(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


# class Menu(BaseSchema):
#     id: str
#     submenus_count: int = 0
#     dishes_count: int = 0
#
#     class Config(BaseSchema.Config):
#         schema_extra = {
#             "example": {
#                 "id": "1",
#                 "title": "Breakfast",
#                 "description": "Breakfast menu description",
#                 "submenus_count": 2,
#                 "dishes_count": 9,
#             },
#         }
#
#
# class MenuCreateUpdate(BaseSchema):
#     class Config(BaseSchema.Config):
#         schema_extra = {
#             "example": {
#                 "title": "Lunch menu",
#                 "description": "Lunch menu description",
#             },
#         }
#

class Submenu(BaseSchema):
    id: str
    dishes_count: int

    class Config(BaseSchema.Config):
        schema_extra = {
            "example": {
                "id": "3",
                "title": "English breakfast",
                "description": "Classic English breakfast description",
                "dishes_count": 8,
            },
        }


class SubmenuCreateUpdate(BaseSchema):
    class Config(BaseSchema.Config):
        schema_extra = {
            "example": {
                "title": "Business lunch",
                "description": "Stonks",
            },
        }


class Dish(BaseSchema):
    id: str
    price: str

    class Config(BaseSchema.Config):
        schema_extra = {
            "example": {
                "id": "5",
                "title": "Chop",
                "description": "Is a dish",
                "price": "9.99",
            },
        }


class DishCreateUpdate(BaseSchema):
    price: str

    class Config(BaseSchema.Config):
        schema_extra = {
            "example": {
                "title": "Chop",
                "description": "Is a dish",
                "price": "9.99",
            },
        }
