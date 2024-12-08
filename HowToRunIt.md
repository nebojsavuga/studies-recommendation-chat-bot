
## Creation of ontology

1. Create virtual environment in python using command:
`py -m venv venv`
2. Activate virtual environment with:
`venv\Scripts\Activate`
3. Install neccessary libraries with:
`pip install -r requirements.txt`
4. Run generate ontology data script with:
`py generate_ontology_data.py`
4. Run generate rdf ontology script with:
`py generate_rdf_ontology.py`

## Openlink virtuoso

1. Pull docker image:
    `docker pull openlink/virtuoso-opensource-7`
2. set password
    `docker run -d -p 8890:8890 -e DBA_PASSWORD=novalozinka openlink/virtuoso-opensource-7`
3. Login with :
`username: dba`
`password: novalozinka`
4. Go to:
`linked data navigation-> Quad Store Upload -> File -> Select ttl file and go upload`

5. Ready to query

## Create embeddings

After uploading ttl file to the virtuoso database you can create embeddings.

1. Activate venv with:
`venv\Scripts\activate`
2. Run command:
`py create_and_save_embeddings.py`

## Run the application

In order to run the application you need to have the openlink virtuoso server running.
You also need an **OPENAI** api key in order to create embeddings and get answers to your questions.

1. Run the backend with:
`py real_server.py`

2. Navigate to front folder, and run the following commands:
- `npm install`
- `ng serve`

Enjoy! :)
