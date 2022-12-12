import pandas as pd
import sparql_dataframe as sd
import json
from flask import current_app
from flaskr.services import triplestore
import logging

#Get all variable names and URI's from the dataset.
def getDatasetUri():
    endpoint = current_app.config.get("rdf_endpoint")
    # endpoint = config["rdf_endpoint"]
    q = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select ?columnName ?colUri
    where { 
	    ?colUri rdfs:subClassOf dbo:ColumnCell;
            dbo:column ?columnName;
            dbo:table ?tableUri.
   	    ?tableUri dbo:table ?tableName.
    }
    """
    df = sd.get(endpoint, q)
    return df

def get_cedar_template_for_dataset_uri(dataset_uri):
    """
    Retrieve the cedar template URI for a given dataset URI
    """
    query = """
    prefix dcat: <http://www.w3.org/ns/dcat#>

    select ?cedar_uri where { 
        ?cedar_uri dcat:distribution [ 
            dcat:identifier "%s"; 
        ].
    }""" % dataset_uri
    logging.debug(query)

    rdfStore = triplestore.GraphDBTripleStore(current_app.config.get("graphdb_server"), current_app.config.get("repository"), create_if_not_exists=True)
    queryResult = rdfStore.select_sparql(query)
    for row in queryResult:
        return row["cedar_uri"]["value"]

#Gets the data of a specific dataset URI
def getData(value):
    endpoint = current_app.config.get("rdf_endpoint")
    # endpoint = config["rdf_endpoint"]
    q = """ 
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    select ?cellValue
    where {{
        ?rowObj dbo:has_column [
            rdf:type <{}>;
            dbo:has_cell [
                dbo:has_value ?cellValue;
            ];
        ].
    }}
    """.format(value)
    df = sd.get(endpoint, q)
    return df

#Get all mapped cell values for a given URI
def getMappedCell(cdmUri, datasetId):
    endpoint = current_app.config.get("rdf_endpoint")
    graph = "http://data.local/mapping/" + datasetId
    # New query
    q = """
        PREFIX owl:<http://www.w3.org/2002/07/owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbo:<http://um-cds/ontologies/databaseontology/>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?categoricalValue ?cellMapping ?cellClass
    WHERE{
                GRAPH <%s>{
                    dbo:cell_of rdf:type owl:ObjectProperty;
                                owl:inverseOf dbo:has_cell.
                                ?cellClass rdf:type owl:Class;
                                       owl:equivalentClass [
                                            owl:intersectionOf([
                                                rdf:type owl:Restriction;
                                                owl:onProperty dbo:cell_of;
                                                owl:someValuesFrom <%s>;
                                            ]
                                            [
                                                rdf:type owl:Restriction;
                                                owl:onProperty dbo:has_value;
                                                owl:hasValue ?categoricalValue;
                                            ]);
                                            rdf:type owl:Class;
                                        ].
                }
        ?cellClass rdfs:label ?cellMapping.
    }

"""%(graph, cdmUri)
    print(q)
    df = sd.get(endpoint, q)
    return df
