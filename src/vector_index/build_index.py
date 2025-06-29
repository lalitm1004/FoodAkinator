from database.models import FoodItem, Question
from sqlmodel import Session, select
import numpy as np
import faiss
import pickle
from database.engine import engine

with Session(engine) as session:
    questions = session.exec(select(Question.id).order_by(Question.id)).all()
    question_to_index = {qid: i for i, qid in enumerate(questions)}
    vector_size = len(questions)

    with open("src/vector_index/question_to_index.pkl", "wb") as f:
        pickle.dump(question_to_index, f)

    food_items = session.exec(select(FoodItem)).all()
    food_vectors = []
    food_id_to_index = {}

    for idx, food in enumerate(food_items):
        vector = np.zeros(vector_size, dtype=np.float32)
        for answer in food.answers:
            q_index = question_to_index[answer.question_id]
            vector[q_index] = answer.value
        food_vectors.append(vector)
        food_id_to_index[food.id] = idx 

    with open("src/vector_index/food_id_map.pkl", "wb") as f:
        pickle.dump(food_id_to_index, f)

    index = faiss.IndexFlatL2(vector_size)
    index.add(np.stack(food_vectors))
    faiss.write_index(index, "src/vector_index/food_index.faiss")