import pandas as pd
import sparql_dataframe as sd

def getDatasetNames():
    endpoint = 'https://graphdb.jvsoest.eu/repositories/epnd_dummy'
    q = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select ?columnName
    where { 
	    ?colUri rdfs:subClassOf dbo:ColumnCell;
            dbo:column ?columnName;
            dbo:table ?tableUri.
   	    ?tableUri dbo:table ?tableName.
    }
    """
    df = sd.get(endpoint, q)
    df = df['columnName']
    return df

def getDatasetUrl(value):
    endpoint = 'https://graphdb.jvsoest.eu/repositories/epnd_dummy'
    q = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select ?colUri ?columnName
    where { 
	    ?colUri rdfs:subClassOf dbo:ColumnCell;
            dbo:column ?columnName;
            dbo:table ?tableUri.
   	    ?tableUri dbo:table ?tableName.
    }
    """

    df = sd.get(endpoint, q)
    df = df.loc[df['columnName'] == value]
    information = df['colUri']
    return information
    
def getDatasetVariables():
    endpoint = 'https://graphdb.jvsoest.eu/repositories/epnd_dummy'
    q = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select ?colUri ?columnName
    where { 
	    ?colUri rdfs:subClassOf dbo:ColumnCell;
            dbo:column ?columnName;
            dbo:table ?tableUri.
   	    ?tableUri dbo:table ?tableName.
    }
    """

    df = sd.get(endpoint, q)
    return df