import pandas as pd
import sparql_dataframe as sd
from SPARQLWrapper import JSON, SPARQLWrapper
import json
from flask import current_app

#Get all variable names and URI's from the dataset.
def getClassCategories(value):
    endpoint = current_app.config.get("rdf_endpoint")
    # endpoint = config["rdf_endpoint"]
    print(value)
    q ='''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX sio: <http://semanticscience.org/resource/>

    SELECT ?categoryLabel
    WHERE
    { BIND (<%s> AS ?targetClass).
      ?nodeShape rdf:type sh:NodeShape;
               sh:targetClass ?targetClass;
               sh:property [
                    sh:path rdf:type;
                    sh:in/rdf:rest*/rdf:first ?category;
               ].
      OPTIONAL
      { ?category rdfs:label ?categoryLabel. }
      FILTER ( ?category != ?targetClass ).
    }'''%value
    df = sd.get(endpoint, q)
    print(df)
    return df
