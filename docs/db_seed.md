# 📄 What The Script Does

1. Archives the existing database (if it exists) by moving it to a timestamped file in `./data/sqlite/archive/`.
2. Creates a new SQLite database at `./data/sqlite/database.db`.
3. Applies schema files (`.sql`) from `./data/sqlite/schema/` to create the necessary tables.
4. Seeds the `food_item` table using CSV files found in `./data/food_items/`. Each CSV represents an outlet.
5. Seeds the `question` table using CSV files found in `./data/questions/`.
6. Populates the `answer` table by combining every food item with every question and assigning an initial answer value of `0`.


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

* The script will ignore other columns.
* Duplicate or empty questions are automatically filtered out.