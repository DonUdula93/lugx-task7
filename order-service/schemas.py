# schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    game_id: str
    user_id: str
    quantity: int

class OrderResponse(OrderCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True  # Updated for Pydantic v2
