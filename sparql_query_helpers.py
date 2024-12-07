import os
import faiss
import json
import requests
import numpy as np

API_URL = "https://api.openai.com/v1/embeddings"
API_KEY = os.getenv("OPENAI_API_KEY")
embedding_file = "data/sparql_query_embeddings.json"


with open("data/sparql_queries.json", "r", encoding="utf-8") as f:
    queries_json = json.load(f)


def load_embeddings(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return np.array(json.load(f), dtype=np.float32)


def save_embeddings(embeddings, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(embeddings.tolist(), f)


def get_embedding(text, model="text-embedding-ada-002"):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"input": text, "model": model}
    response = requests.post(API_URL, headers=headers, json=data)
    response_data = response.json()
    return response_data["data"][0]["embedding"]


def create_embeddings():
    query_embeddings = []
    i = 0
    for query in queries_json["queries"]:
        print(f"Processing embedding for text {i + 1}")
        embedding = get_embedding(query["question"])
        query_embeddings.append(embedding)
        i += 1
    return query_embeddings


def find_best_query(user_question):
    query_embeddings = load_embeddings(embedding_file)
    dimension = len(query_embeddings[0])
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(query_embeddings)
    user_embedding = np.array(get_embedding(user_question), dtype=np.float32).reshape(
        1, -1
    )
    _, indices = faiss_index.search(user_embedding, k=1)
    best_query_index = indices[0][0]
    return (
        queries_json["queries"][best_query_index]["query"],
        queries_json["queries"][best_query_index]["answer_value"],
    )
