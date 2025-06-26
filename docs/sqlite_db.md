# 📦 Database Overview

This document outlines the structure and usage of the database used in this project for managing food items, questions, and their associated ratings (answers).

---

## 🗂️ Purpose

The database supports a structured system to:

* Store **food items** across multiple outlets.
* Maintain a list of **questions** used to describe or evaluate food.
* Capture **answer values** for each `(food item, question)` pair, with a numeric rating between `-2.0` and `+2.0`.

---

## 🏗️ Schema Overview

### 1. `FoodItem`

Represents an individual food item from a particular outlet.

| Field    | Type          | Description                      |
| -------- | ------------- | -------------------------------- |
| `id`     | `int`         | Primary key (auto-generated)     |
| `name`   | `str`         | Name of the food item (required) |
| `outlet` | `Optional[str]` | Name of the outlet (optional)    |

---

### 2. `Question`

Represents a qualitative or quantitative question about food.

| Field  | Type  | Description                  |
| ------ | ----- | ---------------------------- |
| `id`   | `int` | Primary key (auto-generated) |
| `body` | `str` | The question text (required) |

---

### 3. `Answer`

Links a `FoodItem` to a `Question` with a numeric answer.

| Field          | Type    | Description                                              |
| -------------- | ------- | -------------------------------------------------------- |
| `food_item_id` | `int`   | Foreign key referencing `FoodItem.id` (part of PK)       |
| `question_id`  | `int`   | Foreign key referencing `Question.id` (part of PK)       |
| `value`        | `float` | A score between `-2.0` and `+2.0` representing an answer |

**Constraint**: The `value` must always be between `-2.0` and `+2.0`.

---

## ⚙️ Initialization & Seeding

Run the `init_db()` function to:

* Create the SQLite database (if it doesn't exist).
* Set up tables using SQLModel.
* Seed the database with:

  * Food items from CSVs in `data/food_items/`
  * Questions from CSVs in `data/questions/`
  * Default answer rows for all food-question pairs (if not already present)

```python
from database.engine import init_db

init_db()
```

This process is **idempotent**: it will not overwrite or duplicate existing data.

### Ignored Files

Any CSV file in `data/food_items/` whose **filename ends with `.ignore.csv`** will be skipped during seeding. For example, `menu.ignore.csv` will not be processed.

---

# 📁 Expected CSV Formats

## 🥘 Food Items CSVs (`./data/food_items/*.csv`)

Each file represents one outlet (based on the filename) and should contain multiple food items in any column format:

```csv
drinks,veg,non_veg,dessert
Cold Coffee,Veggie,Chicken Steak,Brownie
Oreo Shake,Paneer Wrap,,Chocolate Cake
...
```

* Empty cells are ignored.
* All non-empty strings are inserted as food items.
* The outlet name is derived from the filename (e.g., `burgrill.csv` → outlet = "burgrill").

## ❓ Questions CSVs (`./data/questions/*.csv`)

Each CSV should have a column named `question`, like this:

```csv
question
"Is it spicy?"
"Is it served hot?"
"Is it vegetarian?"
```

---

## 🧵 Session Management

Use the `get_session()` context manager to safely run database queries:

```python
from database.init import get_session
from sqlmodel import select
from database.models import FoodItem

with get_session() as session:
    results = session.exec(select(FoodItem)).all()
```

---

## 🧪 Answer Validation

When inserting into the `Answer` table manually, keep in mind:

* The constructor enforces that the `value` must be between `-2.0` and `+2.0`.
  A `ValueError` will be raised otherwise.

```python
Answer(food_item_id=1, question_id=2, value=1.5)  # ✅ Valid
Answer(food_item_id=1, question_id=2, value=3.0)  # ❌ Raises ValueError
```

---

## 🧼 Best Practices

* Avoid editing the SQLite file manually. Always use SQLModel or SQLAlchemy to interact with it.
* Re-run `init_db()` after adding new food or question CSVs to update the database.
* Use `.ignore.csv` suffix to prevent test or temporary files from being seeded.

---