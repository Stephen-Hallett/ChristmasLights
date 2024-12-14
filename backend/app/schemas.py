from pydantic import BaseModel


class Effects(BaseModel):
    breathing: float
    chasing: float
    decibels: float
    sparkle: float


class Pattern(BaseModel):
    id: int | None = None
    name: str
    pattern: list
    active: bool
    effects: Effects
