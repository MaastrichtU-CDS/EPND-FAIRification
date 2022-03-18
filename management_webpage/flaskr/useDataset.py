from flaskr.db import get_db
import pandas as pd
import sparql_dataframe as sd

def getTableInfo():
    db = get_db()
    information = db.execute('PRAGMA table_info(dataset)').fetchall()
    return information

def getDatabase():
    db = get_db()
    information = db.execute('SELECT * FROM dataset').fetchall()
    return information

def getDataframe():
    db = get_db()
    df = pd.read_sql_query('SELECT * FROM dataset', db)
    return df

def queryDatabase(value):
    db = get_db()
    information = db.execute(value).fetchall()
    return information

def getDatasetNames():
    db = get_db()
    df = pd.read_sql_query('PRAGMA table_info(dataset)', db)
    df = df['name']
    return df

def getTest():
    endpoint = 'https://graphdb.jvsoest.eu/repositories/epnd_dummy'

    q = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    select ?colUri ?columnName ?tableName 
    where { 
	    ?colUri rdfs:subClassOf dbo:ColumnCell;
            dbo:column ?columnName;
            dbo:table ?tableUri.
   	    ?tableUri dbo:table ?tableName.
    }
    """

    df = sd.get(endpoint, q)
    print(df)