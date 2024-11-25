import logging
import sqlite3

from . import schemas

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.connection = sqlite3.connect("../../data/app.db")
        self.cursor = self.connection.cursor()

    def save_pattern(self, pattern: schemas.Pattern) -> str:
        pass

    def list_patterns(self) -> list:
        self.cursor.execute()
