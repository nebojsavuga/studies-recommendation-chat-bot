import json
import rdflib

with open("v3.json", "r", encoding="utf-8") as f:
    program_data = json.load(f)


g = rdflib.Graph()

program_namespace = rdflib.Namespace("http://example.org/program/")
course_namespace = rdflib.Namespace("http://example.org/course/")
ka_namespace = rdflib.Namespace("http://example.org/ka/")
discipline_namespace = rdflib.Namespace("http://example.org/discipline/")

for program_name, program_details in program_data.items():
    program_uri = program_namespace[program_name.replace(" ", "_")]

    g.add((program_uri, program_namespace.has_title, rdflib.Literal(program_details["title"])))
    g.add(
        (
            program_uri,
            program_namespace.has_duration,
            rdflib.Literal(program_details["duration"]),
        )
    )
    g.add(
        (
            program_uri,
            program_namespace.has_type_of_studies,
            rdflib.Literal(program_details["type_of_studies"]),
        )
    )

    # Iterate through courses in the program
    for course in program_details["courses"]:
        course_uri = course_namespace[course["course_name"].replace(" ", "_")]

        # Add course details
        g.add((course_uri, course_namespace.has_name, rdflib.Literal(course["course_name"])))

        # Add knowledge areas for the course
        for ka_data in course["knowledge_areas"]:
            ka_name = ka_data["name"]
            discipline_name = ka_data["discipline"]

            # Create a URI for the knowledge area
            ka_uri = ka_namespace[ka_name.replace(" ", "_")]

            # Check if the Knowledge Area already exists in the graph
            if (ka_uri, None, None) not in g:
                # Add knowledge area as a node
                g.add(
                    (ka_uri, course_namespace.has_knowledge_area_name, rdflib.Literal(ka_name))
                )

            # Link the course to the knowledge area
            g.add((course_uri, course_namespace.has_knowledge_area, ka_uri))

            # Create URI for the discipline
            discipline_uri = discipline_namespace[discipline_name.replace(" ", "_")]

            # Check if the Discipline already exists in the graph
            if (discipline_uri, None, None) not in g:
                # Add discipline as a node
                g.add(
                    (
                        discipline_uri,
                        course_namespace.has_discipline_name,
                        rdflib.Literal(discipline_name),
                    )
                )

            # Link the knowledge area to its corresponding discipline
            g.add((ka_uri, course_namespace.belongs_to_discipline, discipline_uri))
            g.add((discipline_uri, course_namespace.has_knowledge_area, ka_uri))

        g.add((course_uri, course_namespace.has_goal, rdflib.Literal(course["goal"])))
        g.add((course_uri, course_namespace.has_content, rdflib.Literal(course["content"])))
        g.add(
            (
                course_uri,
                course_namespace.has_learning_outcome,
                rdflib.Literal(course["learning_outcome"]),
            )
        )

        g.add((program_uri, course_namespace.has_course, course_uri))

output_path = "program_data_v3.ttl"
g.serialize(destination=output_path, format="turtle")

print(f"RDF data saved to {output_path}")
