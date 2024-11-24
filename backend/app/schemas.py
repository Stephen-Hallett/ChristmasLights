from pydantic import BaseModel


class Effect(BaseModel):
    breathing: int
    chasing: int
    sparkle: int


class Pattern(BaseModel):
    name: str
    pattern: list
    effects: Effect
