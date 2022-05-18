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
    df = sd.get(endpoint, q)
    return df

#get snomed code for selected subclass
def getSnomedCode(sourceValue, selectedValue):
    endpoint = current_app.config.get("rdf_endpoint")
    q = '''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX sio: <http://semanticscience.org/resource/>

    SELECT distinct ?category
    WHERE {
        ## Bind your requested variable to ?targetClass
        BIND (<%s> AS ?targetClass).
        ?nodeShape rdf:type sh:NodeShape;
                 sh:targetClass ?targetClass;
                 sh:property [
                    sh:path rdf:type;
                    # explained in http://www.snee.com/bobdc.blog/2014/04/rdf-lists-and-sparql.html
                    sh:in/rdf:rest*/rdf:first ?category1;
                ].
        BIND(strafter(str(?category1), "http://purl.bioontology.org/ontology/SNOMEDCT/") AS ?category)
        OPTIONAL {
            ?category1 rdfs:label ?categoryLabel.
        }
        FILTER (?category1 != ?targetClass && ?categoryLabel = "%s").
    }'''%(sourceValue, selectedValue)
    df = sd.get(endpoint, q)
    return df
