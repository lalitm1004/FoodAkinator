import sqlite3
import shutil
import time
import pandas as pd
from sqlite3 import Cursor
from typing import Set, List
from pathlib import Path


SQLITE_DB_PATH = Path("./data/sqlite/database.db")
SCHEMA_DIR = Path("./data/sqlite/schema")
FOOD_ITEMS_CSV_DIR = Path("./data/food_items")
QUESTIONS_CSV_DIR = Path("./data/questions")


def apply_schema(cursor: Cursor, schema_dir: Path) -> None:
    print(f"Applying schema from: {schema_dir}")

    sql_files = sorted(schema_dir.glob("*.sql"))
    if not sql_files:
        raise ValueError(f"No .sql files found in {schema_dir}")

    for file in sql_files:
        print(f"\tExecuting: {file.name}")
        sql = file.read_text(encoding="utf-8")
        cursor.executescript(sql)

    print("✅ Schema applied successfully.\n")


def seed_food_item(cursor: Cursor, food_items_csv_dir: Path) -> None:
    print(f"Seeding food items from CSVs in: {food_items_csv_dir}")

    insert_query = "INSERT INTO food_item (name, outlet) VALUES (?, ?)"

    csv_files = food_items_csv_dir.glob("*.csv")
    if not csv_files:
        raise ValueError(f"No .csv files found in {food_items_csv_dir}")

    for file in csv_files:
        outlet_name = file.stem

        df = pd.read_csv(file)

        insert_count = 0
        for value in df.values.ravel():
            if isinstance(value, str):
                cleaned = value.strip()
                if cleaned:
                    cursor.execute(insert_query, (cleaned, outlet_name))
                    insert_count += 1

        print(f"\tInserted {insert_count} items from: {file.name}")

    print("✅ Food items seeded.\n")


def seed_questions(cursor: Cursor, questions_csv_dir: Path) -> None:
    print(f"Seeding food items from CSVs in: {questions_csv_dir}")

    insert_query = "INSERT INTO question (body) VALUES (?)"

    csv_files = questions_csv_dir.glob("*.csv")
    if not csv_files:
        raise ValueError(f"No .csv files found in {questions_csv_dir}")

    all_questions: Set[str] = set()

    for file in csv_files:
        df = pd.read_csv(file)

        if "question" not in df.columns:
            print(f"\tSkipping {file.name} (no 'question' column)")
            continue

        for question in df["question"]:
            if isinstance(question, str):
                cleaned = question.strip().strip('"')
                if cleaned:
                    all_questions.add(cleaned)

    for question in sorted(all_questions):
        cursor.execute(insert_query, (question,))

    print(f"\tInserted {len(all_questions)} questions total.")
    print("✅ Questions seeded.\n")


def seed_answers(cursor: Cursor) -> None:
    print("Populating answer table with default value 0...")

    cursor.execute("SELECT id FROM food_item")
    food_item_ids: List[int] = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM question")
    question_ids: List[int] = [row[0] for row in cursor.fetchall()]

    if not food_item_ids or not question_ids:
        print("\tSkipping: food items or questions are missing.")
        return

    insert_query = (
        "INSERT INTO answer (food_item_id, question_id, value) VALUES (?, ?, 0)"
    )

    count = 0
    for food_id in food_item_ids:
        for question_id in question_ids:
            cursor.execute(insert_query, (food_id, question_id))
            count += 1

    print(f"\tInserted {count} rows into answer table.")
    print("✅ Answers seeded.\n")


def main() -> None:
    print("Initializing SQLite database...")

    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    archive_dir = Path("./data/sqlite/archive")
    archive_dir.mkdir(parents=True, exist_ok=True)

    # Archive db if exists
    if SQLITE_DB_PATH.exists():
        epoch_time = int(time.time())
        archive_path = archive_dir / f"{epoch_time}_database.db"
        shutil.move(str(SQLITE_DB_PATH), str(archive_path))
        print(f"📦 Archived existing database to: {archive_path}")

    with sqlite3.connect(SQLITE_DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        apply_schema(cursor, SCHEMA_DIR)
        seed_food_item(cursor, FOOD_ITEMS_CSV_DIR)
        seed_questions(cursor, QUESTIONS_CSV_DIR)
        seed_answers(cursor)

        connection.commit()

    print(f"🎉 Database initialized and seeded at: '{SQLITE_DB_PATH.resolve()}'")


if __name__ == "__main__":
    main()
