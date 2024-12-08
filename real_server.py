from flask import Flask, request, jsonify
from flask_cors import CORS
from SPARQLWrapper import SPARQLWrapper, JSON
from sparql_query_helpers import find_best_query
from openai import OpenAI
import os

virtuoso_url = "http://localhost:8890/sparql"
sparql = SPARQLWrapper(virtuoso_url)
API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=API_KEY)


def get_formatted_answer(question, results):
    """
    Call the LLM to generate a human-readable response.
    """
    prompt = (
        f"User asked: '{question}'. Based on the following data:\n"
        f"{', '.join(results)}\n"
        "Write a friendly and human-readable answer in Serbian language without excluding any of the data and without markup:"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {e}"


@app.route("/", methods=["POST"])
def get_answer():

    user_input = request.json.get("user_input")

    if not user_input:
        return jsonify({"error": "user_input is required"}), 400

    best_query, answer_value = find_best_query(user_input)

    sparql.setQuery(best_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    response_data = [
        result[answer_value]["value"] for result in results["results"]["bindings"]
    ]
    if response_data:
        human_response = get_formatted_answer(user_input, response_data)
    else:
        human_response = "Izvinjavamo se. Nemamo odgovor na vaše pitanje."
    return jsonify({"response": human_response})


if __name__ == "__main__":
    app.run(debug=True)
