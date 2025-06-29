import faiss
import numpy as np
import pickle

index = faiss.read_index("src/vector_index/food_index.faiss")

with open("src/vector_index/question_to_index.pkl", "rb") as f:
    question_to_index = pickle.load(f)

with open("src/vector_index/food_id_map.pkl", "rb") as f:
    food_id_to_index = pickle.load(f)

index_to_food_id = {v: k for k, v in food_id_to_index.items()}

query_values = {
    1: 1.0,
    2: 1.0
}

m = index.d
query_vector = np.zeros(m, dtype=np.float32)

for qid, val in query_values.items():
    if qid in question_to_index:
        q_index = question_to_index[qid]
        query_vector[q_index] = val

D, I = index.search(query_vector.reshape(1, -1), 5)

print("Top 5 Matches:")
for dist, idx in zip(D[0], I[0]):
    food_id = index_to_food_id.get(idx, "Unknown")
    print(f"Food ID: {food_id} (Distance: {dist:.4f})")