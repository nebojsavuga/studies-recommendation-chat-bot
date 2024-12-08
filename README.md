# Chatbot for program recommendations at the Faculty of Technical Sciences

## Team members

- Bogdan Janošević R2 43/2024
- Kristina Popov Е2 93/2024
- Nebojša Vuga R2 23/2024
## Project goal
The goal of this project is to assist prospective students of the Faculty of Technical Sciences (FTN) in selecting the most suitable study program through an interactive chatbot. By offering personalized recommendations based on students' interests and goals, the chatbot will simplify and improve the decision-making process.

## Curriculum Ontology
The curriculum ontology is a structured model that represents and connects various aspects of academic programs at the Faculty of Technical Sciences (FTN). This ontology is used to organize and understand information about courses, study programs, and their characteristics. We utilized the ACM curriculum guidelines from [CC2020](https://www.acm.org/binaries/content/assets/education/curricula-recommendations/cc2020.pdf) as a basis for designing and structuring the ontology.

### Disciplines and Areas of Knowledge
The curriculum ontology defines the following seven disciplines, each encompassing specific areas of knowledge:
1. [Computer Engineering](https://www.acm.org/binaries/content/assets/education/ce2016-final-report.pdf) - *Circuits and Electronics, Computing Algorithms, Computer Architecture and Organization, Digital Design, Embedded Systems, Computer Networks, Preparation for Professional Practice, Information Security, Signal Processing, Systems and Project Engineering, System Resource Management, Software Design*
2. [Computer Science](https://www.acm.org/binaries/content/assets/education/cs2013_web_final.pdf) - *AL-Algorithms and Complexity, AR-Architecture and Organization, CN-Computational Science, DS-Discrete Structures, GV-Graphics and Visualization, HCI-Human-Computer Interaction, IAS-Information Assurance and Security, IM-Information Management, IS-Intelligent Systems, NC-Networking and Communication, OS-Operating Systems, PBD-Platform-based Development, PD-Parallel and Distributed Computing, PL-Programming Languages, SDF-Software Development Fundamentals, SE-Software Engineering, SF-Systems Fundamentals, SP-Social Issues and Professional Practice*
3. [Cybersecurity](https://www.acm.org/binaries/content/assets/education/curricula-recommendations/csec2017.pdf) -*Data Security, Software Security, Component Security, Connection Security, System Security, Human Security, Organizational Security, Societal Security*
4. [Information Systems](https://www.acm.org/binaries/content/assets/education/curricula-recommendations/is-2010-acm-final.pdf) - *Data and Information Management, Data and Business Analytics, Data and Information Visualization, IT Infrastructure, Secure Computing, Emerging Technologies, Systems Analysis and Design, Application Development and Programming, Object-Orientation, Mobile Development, Web Development, User Interface Design, IS Ethics, Sustainability Use and Implications for Society, IS Management and Strategy, Digital Innovation, Project Management, IS Practicum*
5. [Information Technology](https://www.acm.org/binaries/content/assets/education/curricula-recommendations/it2017.pdf) - *ITE-CSP Cybersecurity Principles,
ITE-GPP Global Professional Practice ,
ITE-IMA Information Management ,
ITE-IST Integrated Systems Technology,
ITE-NET Networking ,
ITE-PFT Platform Technologies ,
ITE-SWF Software Fundamentals ,
ITE-UXD User Experience Design,
ITE-WMS Web and Mobile Systems*
6. [Software Engineering](https://www.acm.org/binaries/content/assets/education/se2014.pdf) - *Software Requirements,
Software Design,
Software Construction,
Software Testing,
Software Sustainment,
Software Process and Life Cycle,
Software Systems Engineering,
Software Quality,
Software Security,
Software Safety,
Software Measurement,
Project Management,
Behavioral Attributes*
7. [Data Science](https://www.acm.org/binaries/content/assets/education/curricula-recommendations/dstf_ccdsc2021.pdf) - *Analysis and Presentation (AP),
Artificial Intelligence (AI),
Big Data Systems (BDS),
Computing and Computer Fundamentals (CCF),
Data Acquisition, Management, and Governance (DG),
Data Mining (DM),
Data Privacy, Security, Integrity, and Analysis for Security (DP),
Machine Learning (ML),
Professionalism (PR),
Programming, Data Structures, and Algorithms (PDA),
Software Development and Maintenance (SDM)*

### Main relations in the Curriculum Ontology
1. Ontology for courses
- hasKnowledgeArea[]:  Connects a course to its associated areas of knowledge.
- hasGoal:  Defines the goal of the course, what students are expected to achieve through its study.
- hasContent:  Describes the content covered by the course.
- hasLearningOutcome:  Specifies the expected learning outcomes for the course.

2. Ontology for study programs
- hasTypeOfStudies:  Connects a study program to its type (e.g., undergraduate academic studies, vocational studies)
- hasTitle:  Specifies the title of the study program.
- hasDuration:  Represents the duration of the study program.
- hasCourses[]:  Connects a study program to the courses included in the program.

We have compiled the details of these disciplines, their associated areas of knowledge, and descriptions into a JSON file. You can find the file at the following path:
- [JSON file with disciplines and knowledge areas](https://github.com/nebojsavuga/studies-recommendation-chat-bot/blob/main/data/data_ACM_ontology.json)

## Data Collection Process
To gather information on programming study programs at the [Faculty of Technical Sciences (FTN)](https://ftn.uns.ac.rs/studijski-programi/), including courses and their details (content, learning outcomes, and goals), we used Python with the Selenium and Beautiful Soup libraries. This allowed us to automate the extraction of structured data from the relevant websites and store it in a structured format for further use. The extracted data was saved in a JSON format, which can be found at the following location:
- [JSON file with study program data](https://github.com/nebojsavuga/studies-recommendation-chat-bot/blob/main/data/course_data.json)

In addition, elective courses were added manually to the JSON file to ensure accuracy and completeness of the data.

## Populating the ACM Ontology with LLM
For mapping academic study programs and their courses to the ACM curriculum, the following ontologies were used:
- OpenAI API: Used for generating textual embeddings for course descriptions and knowledge areas.
- FAISS: Used for creating an index and quickly searching for similarities between course embeddings and knowledge area embeddings.
- Python libraries: ``requests`` , ``faiss``, ``numpy``, and ``json`` for data processing and storage.
 ### Process Steps
 1. Loaded data on programs and courses from ``course_data.json``. Loaded knowledge areas from ``data_ACM_ontology.json``
 2. Extracted course details such as name, goal, content, learning outcomes, type of study, title, and study duration. Extracted knowledge areas from the ACM curriculum.
 3. Used the OpenAI API to create embeddings for course descriptions and knowledge areas. Saved the generated embeddings in ``course_embeddings.json`` and ``ka_embeddings.json``.
 4. Created a FAISS index using the embeddings of the knowledge areas to enable fast similarity searching.
 5. For each course, performed a search in the FAISS index to find the most relevant knowledge areas. Mapped courses to the most relevant knowledge areas based on similarity. Courses were mapped to the top 5 most relevant knowledge areas based on similarity. Specifically, faiss.IndexFlatL2 was used to compute similarities using L2 (Euclidean) distance, enabling efficient nearest neighbor searches.
 6. Combined course data with their corresponding knowledge areas and saved it in ``v3.json``.

## Generating RDF Ontology
This project involves creating an RDF ontology from JSON data that represents academic programs, their courses, and associated knowledge areas. The RDF ontology helps organize and link program data in a structured format, making it suitable for semantic web applications and data integration.

### Steps to generate RDF ontology
1. Load the JSON data from ``v3.json``
2. Use rdflib.Graph() to create an empty RDF graph where data will be added.
3. Define custom namespaces to structure the RDF data for programs, courses, knowledge areas, and disciplines.
4. Create a URI and add properties such as ``has_title``, ``has_duration``, and ``has_type_of_studies``.
5. Create a URI, add details (``has_name``, ``has_goal``, ``has_content``, ``has_learning_outcome``), and link it to the program. Add knowledge areas and link them to the course and related disciplines.
6. Ensure that each knowledge area and discipline is uniquely represented and connected to the relevant courses.
7. Save the RDF graph in Turtle (.ttl) format to a file named ``program_data_v3.ttl``.

The output is an RDF Turtle file (program_data_v3.ttl) that can be used for semantic querying and data integration.
We deployed this ontology to the  [OpenLink Virtuoso database](https://vos.openlinksw.com/owiki/wiki/VOS).

!['Smer'](https://github.com/nebojsavuga/studies-recommendation-chat-bot/blob/develop/smer.png)
!['COurse node'](https://github.com/nebojsavuga/studies-recommendation-chat-bot/blob/develop/course_node.png)
!['Combined knowledge areas'](https://github.com/nebojsavuga/studies-recommendation-chat-bot/blob/develop/knowledge_belong_to_same_discipline.png)


## Querying the Ontology

We created 95 questions that are stored in the ``sparql_queries.json`` file, along with corresponding SPARQL queries and the answer_value tag for identifying the type of answer.
We processed the queries and generated embeddings for the SPARQL queries to enable searching for the best query that matches the user's question. This includes the following steps:

1. Loading data: The file loads the JSON file data/sparql_queries.json, which contains SPARQL queries and their corresponding answers.
2. Generating embeddings: Uses the OpenAI API to generate embeddings for each query in the file. These embeddings are stored in ``data/sparql_query_embeddings.json`` for later use in searching.
3. Saving and loading embeddings: Includes functions for saving embeddings in JSON format and loading them from it.
4. Creating a FAISS index: Utilizes the FAISS library to create an index that enables fast similarity searches between embeddings.
5. Searching for the best query: When a user submits a question, an embedding for that question is generated and compared with all the query embeddings in the FAISS index to find the most relevant query. The query that best matches the user's question and its corresponding answer is returned.

## Server Implementation

This project uses a Flask web server to handle user questions and retrieve answers using SPARQL queries from a Virtuoso database. The server leverages the OpenAI API to generate human-readable responses based on the data retrieved. The SPARQLWrapper library is used to send queries to the Virtuoso database, while custom functions facilitate finding the most relevant query based on user input. The server is set up with CORS support and utilizes environment variables to manage the OpenAI API key securely.

## Frontend

Angular was used to build the user interface that communicates with the backend server, sends user queries, and displays the results obtained from SPARQL queries in real time.
!['chatbot application'](https://github.com/nebojsavuga/studies-recommendation-chat-bot/blob/develop/chatbot.png)
## Running the project

The steps for running the project can be found in ``HowToRunIt.md``. This page contains detailed instructions for installing and running the project, including all necessary steps and configurations to ensure the system is properly set up and functioning.
