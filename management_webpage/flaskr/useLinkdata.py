from flaskr.db import get_db
import pandas as pd
import sparql_dataframe
from flaskr import useDataset

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


