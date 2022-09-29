import pandas as pd
import sparql_dataframe as sd
from SPARQLWrapper import JSON, SPARQLWrapper
import json
from flask import current_app

#Get all variable names and URI's from the dataset.
def getClassCategories(value):
    endpoint = current_app.config.get("rdf_endpoint")
    # endpoint = config["rdf_endpoint"]
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
    print(f"This query is being used for obtaining \
            categories for a given class \n {q}")
    df = sd.get(endpoint, q)
    return df

#get snomed code for selected subclass
def getCategoryCode(sourceValue, selectedValue):
    endpoint = current_app.config.get("rdf_endpoint")
    q = '''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX sio: <http://semanticscience.org/resource/>

    SELECT distinct ?categoryUri 
    WHERE {
        ## Bind your requested variable to ?targetClass
        BIND (<%s> AS ?targetClass).
        ?nodeShape rdf:type sh:NodeShape;
                 sh:targetClass ?targetClass;
                 sh:property [
                    sh:path rdf:type;
                    # explained in http://www.snee.com/bobdc.blog/2014/04/rdf-lists-and-sparql.html
                    sh:in/rdf:rest*/rdf:first ?categoryUri;
                ].
        OPTIONAL {
            ?categoryUri rdfs:label ?categoryLabel.
        }
        ## Remember remember, the casing problem while dealing with strings.
        FILTER (?categoryUri != ?targetClass && ?categoryLabel = LCASE("%s")).
    }'''%(sourceValue, selectedValue)
    print(f"This query is being used for getting the URI\
            for a given category under a class \n {q}")
    df = sd.get(endpoint, q)
    return df
