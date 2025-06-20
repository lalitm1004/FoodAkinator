from dataclasses import dataclass


@dataclass
class FoodItem:
    id: int
    name: str
    outlet: str


@dataclass
class Question:
    id: int
    body: str


@dataclass
class Answer:
    food_item_id: int
    question_id: int
    value: int

    def __post_init__(self) -> None:
        if not -2 <= self.value <= 2:
            raise ValueError("value must be between -2 and 2")
