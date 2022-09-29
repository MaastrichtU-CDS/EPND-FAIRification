import pandas as pd
import sparql_dataframe as sd
from flask import current_app

#Gets the Uri and names from the entries in the CDM
def getCDMUri():
    endpoint = current_app.config.get("rdf_endpoint")
    q = """
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix sh: <http://www.w3.org/ns/shacl#>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    prefix sio: <http://semanticscience.org/resource/>

    SELECT DISTINCT ?variableUri ?variableUriLabel
    WHERE {
        ?nodeShape rdf:type sh:NodeShape;
            sh:targetClass ?variableUri.

        OPTIONAL {
            ?variableUri rdfs:label ?variableUriLabel.
        }
        
        # If only binary/numeric/categoric variables are allowed, disable the optional here
        OPTIONAL {
            ?nodeShape rdf:type ?variableType.
            ?variableType rdfs:label ?variableTypeLabel.
            FILTER (?variableType IN (sio:SIO_000137, sio:SIO_000915, sio:SIO_000914)).
        }
        
        ## Units are always their own instance (measurement -> unit -> literal), therefore filtering the unit instances.
        FILTER (!(STRSTARTS(str(?variableUri), "http://purl.obolibrary.org/obo/UO_"))).
        ## This filter will have be modified based on changes in the future.
        ## Another one might have to be added is schema1:Date depending on the
        ## role it plays
        FILTER (?variableUri != sio:SIO_001112 && ?variableUri != sty:T081 && ?variableUri != sty:T079 && ?variableUri != sty:T080).
        
    }
    """

    df = sd.get(endpoint, q)
    return df

#Gets all information included in the CDM
def getCDMFull():
    endpoint = current_app.config.get("rdf_endpoint")
    q = """
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix sh: <http://www.w3.org/ns/shacl#>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    prefix sio: <http://semanticscience.org/resource/>

    SELECT ?nodeShape ?variableUri ?variableUriLabel ?variableType ?variableTypeLabel
    WHERE {
        ?nodeShape rdf:type sh:NodeShape;
            sh:targetClass ?variableUri.

        OPTIONAL {
            ?variableUri rdfs:label ?variableUriLabel.
        }
        
        # If only binary/numeric/categoric variables are allowed, disable the optional here
        OPTIONAL {
            ?nodeShape rdf:type ?variableType.
            ?variableType rdfs:label ?variableTypeLabel.
            FILTER (?variableType IN (sio:SIO_000137, sio:SIO_000915, sio:SIO_000914)).
        }
        
        ## Units are always their own instance (measurement -> unit -> literal), therefore filtering the unit instances.
        FILTER (!(STRSTARTS(str(?variableUri), "http://purl.obolibrary.org/obo/UO_"))).
        FILTER (?variableUri != sio:SIO_001112).
        
    }
    """
    df = sd.get(endpoint, q)
    return df
