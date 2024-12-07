from flask import Flask, request, jsonify
from flask_cors import CORS
from SPARQLWrapper import SPARQLWrapper, JSON
from sparql_query_helpers import find_best_query

virtuoso_url = "http://localhost:8890/sparql"
sparql = SPARQLWrapper(virtuoso_url)

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def get_answer():
    
    user_input = request.json.get("user_input")

    if not user_input:
        return jsonify({"error": "user_input is required"}), 400

    best_query, answer_value = find_best_query(user_input)

    sparql.setQuery(best_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    response_data = []
    for result in results["results"]["bindings"]:
        response_data.append(result[answer_value]["value"])

    return jsonify({"results": response_data})


if __name__ == "__main__":
    app.run(debug=True)
