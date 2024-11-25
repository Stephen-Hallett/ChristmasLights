from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import schemas
from .config import settings
from .controller import Controller

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


con = Controller()


@app.post("/patterns/save")
def save_pattern(pattern: schemas.Pattern) -> str:
    return con.save_pattern(pattern=pattern)


@app.get("/patterns/list")
def list_patterns() -> list[schemas.Pattern]:
    return con.list_patterns()


@app.get("/patterns/get/{id}")
def get_pattern(id: int) -> schemas.Pattern:
    return con.get_pattern(id)


@app.get("/test")
def test() -> str:
    return "What up big dog"
