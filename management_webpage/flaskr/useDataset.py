import pandas as pd
import sparql_dataframe as sd
from SPARQLWrapper import JSON, SPARQLWrapper

#Get all variable names and URI's from the dataset.
def getDatasetUri():
    endpoint = 'https://graphdb.jvsoest.eu/repositories/epnd_dummy'
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

def getData(value):
    endpoint = 'https://graphdb.jvsoest.eu/repositories/epnd_dummy'
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

def othertry(valueList):
    for value in valueList:
        try:
            endpoint = SPARQLWrapper('https://graphdb.jvsoest.eu/repositories/epnd_dummy')
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
            """.format(value[3])
            print(value[3])
            endpoint.setQuery(q)
            endpoint.method = 'GET'
            endpoint.setReturnFormat(JSON)
            a = endpoint.query().convert()
            print('soep')
            print(a[0])
            
        except:
            pass