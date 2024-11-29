from typing import Optional

from pydantic import BaseModel


class Effects(BaseModel):
    breathing: float
    chasing: float
    sparkle: int


class Pattern(BaseModel):
    id: Optional[int] = None
    name: str
    pattern: list
    active: bool
    effects: Effects
