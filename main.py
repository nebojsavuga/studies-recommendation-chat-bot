import openai
import faiss
import numpy as np
import json
import requests
import os

API_URL = "https://api.openai.com/v1/embeddings"
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY
def save_embeddings(embeddings, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(embeddings, f)

def get_embedding(text, model="text-embedding-ada-002"):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {"input": text, "model": model}
    response = requests.post(API_URL, headers=headers, json=data)
    response_data = response.json()
    return response_data["data"][0]["embedding"]


def generate_embeddings(texts):
    embeddings = []
    i = 0
    for text in texts:
        print(f"Processing embedding for text {i + 1}/{len(texts)}")
        embedding = get_embedding(text)
        embeddings.append(embedding)
        if (i + 1) % 10 == 0:
            print(f"Generated {i + 1}/{len(texts)} embeddings.")
        i += 1
    return embeddings


print("Loading data...")
with open("data/course_data.json", "r", encoding="utf-8") as f:
    course_data = json.load(f)

with open("data/data_ACM_ontology.json", "r", encoding="utf-8") as f:
    acm_data = json.load(f)
print("Data loaded successfully.")

courses = []
knowledge_areas = []
print("Extracting course and knowledge area data...")

for program_name, program_details in course_data.items():
    for subject in program_details.get("Predmeti", []):
        courses.append(
            {
                "name": subject["ime"],
                "description": f"{subject['cilj']} {subject['ishod']} {subject['sadrzaj']}",
                "course": program_name,
                "goal": subject["cilj"],
                "content": subject["sadrzaj"],
                "learning_outcome": subject["ishod"],
                "type_of_studies": program_details.get("Stepen i vrsta studija", ""),
                "title": program_details.get("Zvanje koje se stiče", ""),
                "duration": program_details.get("Trajanje (god/sem)", ""),
            }
        )
    for key, value in program_details.items():
        if key.startswith("Izbor") and isinstance(value, list):
            for subject in value:
                if isinstance(subject, dict) and "ime" in subject:
                    courses.append(
                        {
                            "name": subject["ime"],
                            "description": f"{subject['cilj']} {subject['ishod']} {subject['sadrzaj']}",
                            "course": program_name,
                            "goal": subject["cilj"],
                            "content": subject["sadrzaj"],
                            "learning_outcome": subject["ishod"],
                            "type_of_studies": program_details.get(
                                "Stepen i vrsta studija", ""
                            ),
                            "title": program_details.get("Zvanje koje se stiče", ""),
                            "duration": program_details.get("Trajanje (god/sem)", ""),
                        }
                    )
print(f"Extracted {len(courses)} courses.")

for domain, domain_details in acm_data.items():
    for ka in domain_details["knowledge_areas"]:
        knowledge_areas.append({"name": ka["name"], "description": ka["description"]})
print(f"Extracted {len(knowledge_areas)} knowledge areas.")

print("Generating embeddings for courses...")

course_embeddings = generate_embeddings([course["description"] for course in courses])
save_embeddings(course_embeddings, 'course_embeddings.json')
print("Course embeddings generated successfully.")
print("Generating embeddings for knowledge areas...")

ka_embeddings = generate_embeddings([ka["description"] for ka in knowledge_areas])
save_embeddings(ka_embeddings, 'ka_embeddings.json')
print("Knowledge area embeddings generated successfully.")

print("Creating FAISS index...")

dimension = len(course_embeddings[0])
faiss_index = faiss.IndexFlatL2(dimension)

ka_metadata = [
    {"name": ka["name"], "description": ka["description"]} for ka in knowledge_areas
]
faiss_index.add(np.array(ka_embeddings, dtype=np.float32))
print("FAISS index created and populated with knowledge area embeddings.")

print("Mapping courses to knowledge areas...")
program_courses = {}
for i, course in enumerate(courses):
    query_embedding = np.array(course_embeddings[i], dtype=np.float32).reshape(1, -1)
    distances, indices = faiss_index.search(query_embedding, k=3)  # Top 3 KA
    top_matches = [ka_metadata[idx]["name"] for _, idx in enumerate(indices[0])]

    program_name = course["course"]
    title = course["title"]
    duration = course["duration"]
    type_of_studies = course["type_of_studies"]

    if program_name not in program_courses:
        program_courses[program_name] = {
            "title": title,
            "duration": duration,
            "type_of_studies": type_of_studies,
            "courses": [],
        }
    program_courses[program_name]["courses"].append(
        {
            "course_name": course["name"],
            "knowledge_areas": top_matches,
            "goal": course["goal"],
            "content": course["content"],
            "learning_outcome": course["learning_outcome"],
        }
    )
print("Course mapping completed.")

output_path = "v2.json"
print(f"Saving results to {output_path}...")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(program_courses, f, ensure_ascii=False, indent=4)

print(f"Rezultati su sačuvani u {output_path}")
