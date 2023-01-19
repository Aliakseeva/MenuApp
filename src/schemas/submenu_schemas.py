from pydantic import BaseModel


class Submenu(BaseModel):
    id: str
    title: str
    description: str
    dishes_count: int

    class Config:
        orm_mode = True


class SubmenuCreateUpdate(BaseModel):
    title: str
    description: str
