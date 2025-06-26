from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional


class FoodItem(SQLModel, table=True):
    """
    Represents a food item available from a specific outlet

    Attributes
        id `Optional[int]`: Auto-generated primary key for the food item
        name `str`: Name of the food item
        outlet `Optional[str]`: Name of the outlet the food item belongs to
        answers `List[Answer]`: List of answers linking this food item to questions
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    outlet: Optional[str] = None
    answers: List["Answer"] = Relationship(back_populates="food_item")


class Question(SQLModel, table=True):
    """
    Represents a food item available from a specific outlet

    Attributes
        id `Optional[int]`: Auto-generated primary key for the question
        body `str`: Question body
        answers `List[Answer]`: List of answers linking this question to food items
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    body: str = Field(nullable=False)
    answers: List["Answer"] = Relationship(back_populates="question")


class Answer(SQLModel, table=True):
    """
    Represents an answer to a question for a specific food item.

    This forms a many-to-many relationship between `FoodItem` and `Question`, with
    an associated numeric value representing the answer.

    Attributes
        question_id `int`: Foreign key referencing the related Question.
        food_item_id `int`: Foreign key referencing the related FoodItem.
        value `float`: A numeric value representing the answer, must be between -2.0 and 2.0 inclusive.
        question `Question`: Relationship to the associated Question.
        food_item `FoodItem`: Relationship to the associated FoodItem.
    """

    question_id: int = Field(foreign_key="question.id", primary_key=True)
    food_item_id: int = Field(foreign_key="fooditem.id", primary_key=True)
    value: float = Field(nullable=False)

    question: Question = Relationship(back_populates="answers")
    food_item: FoodItem = Relationship(back_populates="answers")

    def __init__(
        self, *, question_id: int, food_item_id: int, value: float, **kwargs
    ) -> None:
        if not (-2.0 <= value <= 2.0):
            raise ValueError(
                f"Invalid answer value: {value} for question_id={question_id}, food_item_id={food_item_id}. "
                "Value must be between -2.0 and +2.0 inclusive."
            )

        super().__init__(
            question_id=question_id, food_item_id=food_item_id, value=value, **kwargs
        )
