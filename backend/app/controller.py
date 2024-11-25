import json
import logging
import os
import sqlite3

from . import schemas

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.db_path = os.environ.get("DATABASE_PATH ", "../data/app.db")

    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _make_pattern_dict(self, item: sqlite3.Row) -> dict:
        item = dict(item)
        item["pattern"] = json.loads(item["pattern"])
        item["effects"] = {
            key: item.pop(key) for key in schemas.Effects.model_fields.keys()
        }
        return item

    def _make_db_row(self, pattern: schemas.Pattern) -> tuple[dict, dict]:
        pattern = pattern.dict()
        pattern.pop("id")
        effect_item = pattern.pop("effects")
        pattern["pattern"] = json.dumps(pattern["pattern"])
        pattern_sorted = {key: pattern[key] for key in sorted(pattern)}
        effect_item_sorted = {key: effect_item[key] for key in sorted(effect_item)}

        return tuple(pattern_sorted.values()), tuple(effect_item_sorted.values())

    def save_pattern(self, pattern: schemas.Pattern) -> str:
        pattern_values, effect_values = self._make_db_row(pattern)
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Patterns (name, pattern) VALUES (?, ?)", pattern_values
        )
        last_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO Effects (id, breathing, chasing, sparkle) VALUES (?, ?, ?, ?)",
            (last_id, *effect_values),
        )
        conn.commit()
        conn.close()
        return f"Pattern #{last_id} saved."

    def list_patterns(self) -> list:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM (Patterns INNER JOIN Effects USING(id))")
        res = cursor.fetchall()
        conn.close()
        return [self._make_pattern_dict(item) for item in res]

    def get_pattern(self, id: int) -> list:
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM (Patterns INNER JOIN Effects USING(id)) WHERE id = ?", (id,)
        )
        res = cursor.fetchone()
        conn.close()
        return self._make_pattern_dict(res)
