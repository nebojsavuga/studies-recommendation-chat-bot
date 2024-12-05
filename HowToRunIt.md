
## Backend

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