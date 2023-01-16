from pydantic import BaseModel


class Submenu(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuCreate(BaseModel):
    title: str
    description: str


class SubmenuUpdate(BaseModel):
    title: str
    description: str
