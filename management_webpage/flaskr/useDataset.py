import pandas as pd
import sparql_dataframe as sd
from SPARQLWrapper import JSON, SPARQLWrapper
import json
from flask import current_app

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
def getMappedCell(cdmUri):
    endpoint = current_app.config.get("rdf_endpoint")
    graph = "http://data.local/mapping"
    print(cdmUri)
    q = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT ?categoricalValue ?cellMapping
    WHERE{
        {
            SELECT ?node ?categoricalValue
            WHERE {
                GRAPH <%s>{
                    ?node owl:equivalentClass[
                          rdf:type owl:Class;
                          owl:intersectionOf[
                                rdf:first <%s>;
                                rdf:rest[
                                    rdf:first[
                                        rdf:type owl:Class;
                                        owl:unionOf[
                                            rdf:first[
                                                rdf:type owl:Restriction;
                                                owl:hasValue ?categoricalValue;
                                                owl:onProperty dbo:has_value;
                                            ];
                                        rdf:rest rdf:nil;
                                        ]
                                    ];
                                    rdf:rest rdf:nil;
                                ]
                        ]
                    ].
                }
            }
        }
        ?node rdfs:label ?cellMapping

    }"""%(graph, cdmUri)
    df = sd.get(endpoint, q)
    return df
