import pandas as pd
import sparql_dataframe as sd
from SPARQLWrapper import SPARQLWrapper
from flask import current_app

#Add a new link
def createLink(value1, value2):
    endpointUrl = current_app.config.get("rdf_endpoint")
    endpoint = SPARQLWrapper(endpointUrl + '/statements')
    q = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
insert {{
    GRAPH <http://mapping.local/> {{
        <{}>
            owl:equivalentClass <{}>
        }}
    }} where {{ }}
    """.format(value1, value2)
    endpoint.setQuery(q)
    endpoint.method = 'POST'
    endpoint.query()

#Delete a existing link
def deleteLink(value1, value2):
    print('start deletion')
    print(value1)
    print(value2)
    endpointUrl = current_app.config.get("rdf_endpoint")
    endpoint = SPARQLWrapper(endpointUrl + '/statements')
    q = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
delete {{
    GRAPH <http://mapping.local/> {{
        <{}> owl:equivalentClass <{}>
    }}
}} where {{ }} 

    """.format(value1, value2)
    endpoint.setQuery(q)
    endpoint.method = 'POST'
    endpoint.query()
    print('end deletion')

#Retrieves all mapped values
def retrieveMappings():
    endpoint = current_app.config.get("rdf_endpoint")
    q = """
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix sh: <http://www.w3.org/ns/shacl#>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    prefix sio: <http://semanticscience.org/resource/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>

    SELECT ?cdmUri ?cdmUriLabel ?columnName ?columnUri
    WHERE {
                GRAPH <http://mapping.local/> {
                ?columnUri owl:equivalentClass ?cdmUri
            }
                ?columnUri rdfs:subClassOf dbo:ColumnCell;
                    dbo:column ?columnName;
                    dbo:table ?tableUri.
                ?tableUri dbo:table ?tableName.
        
        ?nodeShape rdf:type sh:NodeShape;
            sh:targetClass ?cdmUri.

        OPTIONAL {
            ?cdmUri rdfs:label ?cdmUriLabel.
        }

        
        ## Units are always their own instance (measurement -> unit -> literal), therefore filtering the unit instances.
        FILTER (!(STRSTARTS(str(?cdmUri), "http://purl.obolibrary.org/obo/UO_"))).
        FILTER (?cdmUri != sio:SIO_001112).
    }
    """
    df = sd.get(endpoint, q)
    return df

#Retrieves the dataset columns both mapped and not mapped
def retrieveDatasetMapped():
    print(current_app.config)
    endpoint = current_app.config.get("rdf_endpoint")
    q = """    
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix sh: <http://www.w3.org/ns/shacl#>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    prefix sio: <http://semanticscience.org/resource/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>

    SELECT ?cdmUri ?cdmUriLabel ?columnName ?columnUri
    WHERE {
    
    	    ?columnUri rdfs:subClassOf dbo:ColumnCell;
            dbo:column ?columnName;
            dbo:table ?tableUri.
   	    ?tableUri dbo:table ?tableName.
    optional{
                GRAPH <http://mapping.local/> {
                ?columnUri owl:equivalentClass ?cdmUri
            }
                ?columnUri rdfs:subClassOf dbo:ColumnCell;
                    dbo:column ?columnName;
                    dbo:table ?tableUri.
                ?tableUri dbo:table ?tableName.
        
        ?nodeShape rdf:type sh:NodeShape;
            sh:targetClass ?cdmUri.

        OPTIONAL {
            ?cdmUri rdfs:label ?cdmUriLabel.
        }

        
        ## Units are always their own instance (measurement -> unit -> literal), therefore filtering the unit instances.
        FILTER (!(STRSTARTS(str(?cdmUri), "http://purl.obolibrary.org/obo/UO_"))).
        FILTER (?cdmUri != sio:SIO_001112).}
    }"""
    df = sd.get(endpoint, q)
    return df

