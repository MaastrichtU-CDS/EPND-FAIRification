from flaskr.db import get_db
import pandas as pd
import sparql_dataframe
from flaskr import useDataset
from SPARQLWrapper import SPARQLWrapper

def getDatabase():
    db = get_db()
    information = db.execute('SELECT * FROM linkedTable').fetchall()
    return information

def getDataframe():
    db = get_db()
    df = pd.read_sql_query('SELECT * FROM linkedTable', db)
    return df


def queryDatabase(value):
    db = get_db()
    information = db.execute(value).fetchall()
    return information

def newLink(value1, value2):
    db = get_db()
    addLink(value1, value2)
    db.execute("INSERT INTO linkedTable (datacolumn, cdmcolumn) VALUES (?, ?)", (value1, value2))
    db.commit()
    
def deleteLink(value1):
    db = get_db()
    db.execute("DELETE FROM linkedTable WHERE datacolumn=?", (value1,))
    db.commit()

def getDataframeTest():
    db = get_db
    df = pd.read_sql_query('SELECT * FROM linkedTable, db')
    df2 = useDataset.getDatasetVariables()

#Add a new link
def addLink(value1, value2):
    value1 = "http://"+value1
    value2 = "http://"+value2

    endpoint = SPARQLWrapper('https://graphdb.jvsoest.eu/repositories/epnd_dummy/statements')
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
def delLink(value1, value2):
    value1 = "http://"+value1
    value2 = "http://"+value2
    endpoint = SPARQLWrapper('https://graphdb.jvsoest.eu/repositories/epnd_dummy/statements')
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

def test():
    print('a')

