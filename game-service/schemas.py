from pydantic import BaseModel
from typing import Optional

class GameBase(BaseModel):
    title: str
    genre: str
    price: float

class GameCreate(GameBase):
    pass

class GameOut(GameBase):
    id: int

    class Config:
        orm_mode = True
