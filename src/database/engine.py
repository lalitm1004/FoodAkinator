import pandas as pd
from contextlib import contextmanager
from pathlib import Path
from sqlmodel import SQLModel, Session, create_engine, select
from typing import Final, Generator, Set

from database.models import FoodItem, Question, Answer


db_path: Final[Path] = Path("data/sqlite/database.db").resolve()
DATABASE_URL: Final[str] = f"sqlite:///{db_path.as_posix()}"

FOOD_ITEMS_CSV_DIR: Final[Path] = Path("data/food_items")
QUESTIONS_CSV_DIR: Final[Path] = Path("data/questions")

engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """
    Initialize the database schema and seed it with data from CSV files.

    This function:
    - Creates all tables defined in the SQLModel metadata (if they don't exist).
    - Loads food items from CSVs in the `FOOD_ITEMS_CSV_DIR` directory and inserts new items.
    - Loads questions from CSVs in the `QUESTIONS_CSV_DIR` directory and inserts new questions.
    - For every food item and question pair, inserts an Answer record with default value `0.0`, if such a record does not already exist.

    The operation is idempotent: running it multiple times does not modify or duplicate data.
    """

    db_path.parent.mkdir(parents=True, exist_ok=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Seed Food Items
        food_files = list(FOOD_ITEMS_CSV_DIR.glob("*.csv"))
        existing_items = session.exec(select(FoodItem)).all()
        existing_set = {(f.name.strip(), f.outlet) for f in existing_items}

        for file in food_files:
            if file.stem.endswith(".ignore"):
                continue

            outlet = file.stem
            df = pd.read_csv(file)

            for value in df.values.ravel():
                if isinstance(value, str):
                    name = value.strip()
                    if name and (name, outlet) not in existing_set:
                        session.add(FoodItem(name=name, outlet=outlet))
                        existing_set.add((name, outlet))

        # Seed Questions
        question_files = list(QUESTIONS_CSV_DIR.glob("*.csv"))
        all_questions: Set[str] = set()

        for file in question_files:
            df = pd.read_csv(file)
            if "question" in df.columns:
                for q in df["question"]:
                    if isinstance(q, str):
                        cleaned = q.strip().strip('"')
                        if cleaned:
                            all_questions.add(cleaned)

        existing_questions = session.exec(select(Question)).all()
        existing_set = {q.body.strip() for q in existing_questions}

        for question in sorted(all_questions):
            if question not in existing_set:
                session.add(Question(body=question))
                existing_set.add(question)

        session.commit()

        # Re-fetch to get auto-generated IDs
        food_items = session.exec(select(FoodItem)).all()
        questions = session.exec(select(Question)).all()
        existing_answers = session.exec(select(Answer)).all()
        existing_keys = {(a.food_item_id, a.question_id) for a in existing_answers}

        # Build answer entries only if not already present
        for food in food_items:
            for question in questions:
                key = (food.id, question.id)
                if key not in existing_keys:
                    session.add(
                        Answer(food_item_id=food.id, question_id=question.id, value=0.0)
                    )

        session.commit()


@contextmanager
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
