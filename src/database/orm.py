import sqlite3
from typing import List, Optional

from models import Answer, FoodItem, Question


class FoodItemTable:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def fetch_all(self) -> List[FoodItem]:
        cursor = self.conn.execute("SELECT * FROM food_item")
        return [FoodItem(**dict(row)) for row in cursor.fetchall()]

    def fetch_by_id(self, id: int) -> Optional[FoodItem]:
        cursor = self.conn.execute("SELECT * FROM food_item WHERE id = ?", (id,))
        row = cursor.fetchone()
        return FoodItem(**dict(row)) if row else None

    def fetch_by_outlet(self, outlet: str) -> List[FoodItem]:
        cursor = self.conn.execute(
            "SELECT * FROM food_item WHERE outlet = ?", (outlet,)
        )
        return [FoodItem(**dict(row)) for row in cursor.fetchall()]

    def insert(self, name: str, outlet: str) -> None:
        self.conn.execute(
            "INSERT INTO food_item (name, outlet) VALUES (?, ?)", (name, outlet)
        )
        self.conn.commit()

    def update(self, id: int, name: str, outlet: str) -> None:
        self.conn.execute(
            "UPDATE food_item SET name = ?, outlet = ? WHERE id = ?", (name, outlet, id)
        )
        self.conn.commit()

    def delete(self, id: int) -> None:
        self.conn.execute("DELETE FROM food_item WHERE id = ?", (id,))
        self.conn.commit()


class QuestionTable:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def fetch_all(self) -> List[Question]:
        cursor = self.conn.execute("SELECT * FROM question")
        return [Question(**dict(row)) for row in cursor.fetchall()]

    def fetch_by_id(self, id: int) -> Optional[Question]:
        cursor = self.conn.execute("SELECT * FROM question WHERE id = ?", (id,))
        row = cursor.fetchone()
        return Question(**dict(row)) if row else None

    def insert(self, body: str) -> None:
        self.conn.execute("INSERT INTO question (body) VALUES (?)", (body,))
        self.conn.commit()

    def update(self, id: int, body: str) -> None:
        self.conn.execute("UPDATE question SET body = ? WHERE id = ?", (body, id))
        self.conn.commit()

    def delete(self, id: int) -> None:
        self.conn.execute("DELETE FROM question WHERE id = ?", (id,))
        self.conn.commit()


class AnswerTable:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def fetch(self, food_item_id: int, question_id: int) -> Optional[Answer]:
        cursor = self.conn.execute(
            "SELECT * FROM answer WHERE food_item_id = ? AND question_id = ?",
            (food_item_id, question_id),
        )
        row = cursor.fetchone()
        return Answer(**dict(row)) if row else None

    def fetch_by_question_id(self, question_id: int) -> List[Answer]:
        cursor = self.conn.execute(
            "SELECT * FROM answer WHERE question_id = ?", (question_id,)
        )
        return [Answer(**dict(row)) for row in cursor.fetchall()]

    def fetch_by_food_item_id(self, food_item_id: int) -> List[Answer]:
        cursor = self.conn.execute(
            "SELECT * FROM answer WHERE food_item_id = ?", (food_item_id,)
        )
        return [Answer(**dict(row)) for row in cursor.fetchall()]

    def fetch_by_value(self, value: int) -> List[Answer]:
        cursor = self.conn.execute("SELECT * FROM answer WHERE value = ?", (value,))
        return [Answer(**dict(row)) for row in cursor.fetchall()]

    def insert(self, food_item_id: int, question_id: int, value: int) -> None:
        self.conn.execute(
            "INSERT INTO answer (food_item_id, question_id, value) VALUES (?, ?, ?)",
            (food_item_id, question_id, value),
        )
        self.conn.commit()

    def update_value(self, food_item_id: int, question_id: int, value: int) -> None:
        self.conn.execute(
            "UPDATE answer SET value = ? WHERE food_item_id = ? AND question_id = ?",
            (value, food_item_id, question_id),
        )
        self.conn.commit()

    def delete(self, food_item_id: int, question_id: int) -> None:
        self.conn.execute(
            "DELETE FROM answer WHERE food_item_id = ? AND question_id = ?",
            (food_item_id, question_id),
        )
        self.conn.commit()


class Database:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.FoodItem = FoodItemTable(self.conn)
        self.Question = QuestionTable(self.conn)
        self.Answer = AnswerTable(self.conn)

    def __del__(self) -> None:
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
