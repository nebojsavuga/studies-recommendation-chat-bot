import json
import rdflib

with open("v2.json", "r", encoding="utf-8") as f:
    program_data = json.load(f)


g = rdflib.Graph()

namespace = rdflib.Namespace("http://example.org/")
for program_name, program_details in program_data.items():
    program_uri = namespace[program_name.replace(" ", "_")]

    g.add((program_uri, namespace.has_title, rdflib.Literal(program_details["title"])))
    g.add(
        (
            program_uri,
            namespace.has_duration,
            rdflib.Literal(program_details["duration"]),
        )
    )
    g.add(
        (
            program_uri,
            namespace.has_type_of_studies,
            rdflib.Literal(program_details["type_of_studies"]),
        )
    )

    # Iterate through courses in the program
    for course in program_details["courses"]:
        course_uri = namespace[course["course_name"].replace(" ", "_")]

        # Add course details
        g.add((course_uri, namespace.has_name, rdflib.Literal(course["course_name"])))

        # Add knowledge areas for the course
        for ka in course["knowledge_areas"]:
            g.add((course_uri, namespace.has_knowledge_area, rdflib.Literal(ka)))

        g.add((course_uri, namespace.has_goal, rdflib.Literal(course["goal"])))
        g.add((course_uri, namespace.has_content, rdflib.Literal(course["content"])))
        g.add(
            (
                course_uri,
                namespace.has_learning_outcome,
                rdflib.Literal(course["learning_outcome"]),
            )
        )

        g.add((program_uri, namespace.has_course, course_uri))

output_path = "program_data.ttl"
g.serialize(destination=output_path, format="turtle")

print(f"RDF data saved to {output_path}")
