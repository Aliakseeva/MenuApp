from pydantic import BaseModel


class Submenu(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuCreate(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int = 0


class SubmenuUpdate(BaseModel):
    title: str
    description: str
