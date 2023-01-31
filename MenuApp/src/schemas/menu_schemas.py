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
            'example': {
                'id': '0921',
                'title': 'Breakfast',
                'description': 'Breakfast menu description',
                'submenus_count': 2,
                'dishes_count': 9,
            },
        }


class MenuCreateUpdate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Lunch menu',
                'description': 'Lunch menu description',
            },
        }
