from pydantic import BaseModel


class Submenu(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "1000",
                "title": "English breakfast",
                "description": "Classic English breakfast description",
                "dishes_count": 8,
            },
        }


class SubmenuCreateUpdate(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "title": "Business lunch",
                "description": "Stonks",
            },
        }
