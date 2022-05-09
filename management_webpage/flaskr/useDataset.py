import pandas as pd
import sparql_dataframe as sd
from SPARQLWrapper import JSON, SPARQLWrapper
import json

config = { }
with open("config.json") as f:
    config = json.load(f)

#Get all variable names and URI's from the dataset.
def getDatasetUri():
    endpoint = config["rdf_endpoint"]
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
    endpoint = config["rdf_endpoint"]
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