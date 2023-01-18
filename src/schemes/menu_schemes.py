from pydantic import BaseModel


class Menu(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class MenuCreateUpdate(BaseModel):
    title: str
    description: str

