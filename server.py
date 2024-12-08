from SPARQLWrapper import SPARQLWrapper, JSON
from sparql_query_helpers import find_best_query

virtuoso_url = "http://localhost:8890/sparql"
sparql = SPARQLWrapper(virtuoso_url)
while(True):
    user_input = input("Postavite pitanje: ")
    if(user_input == "x"):
        break
    best_query, answer_value = find_best_query(user_input)
    sparql.setQuery(f"{best_query}")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        print(f"{result[answer_value]['value']}")
