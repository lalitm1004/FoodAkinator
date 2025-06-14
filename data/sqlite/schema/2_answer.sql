DROP TABLE IF EXISTS answer;

CREATE TABLE answer (
    question_id INTEGER NOT NULL,
    food_item_id INTEGER NOT NULL,
    value INTEGER NOT NULL CHECK(value IN (-2, -1, 0, 1, 2)),
    PRIMARY KEY (question_id, food_item_id),
    FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE,
    FOREIGN KEY (food_item_id) REFERENCES food_item(id) ON DELETE CASCADE
);