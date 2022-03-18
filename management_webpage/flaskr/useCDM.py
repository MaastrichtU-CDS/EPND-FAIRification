from flaskr.db import get_db
import pandas as pd
import sparql_dataframe

def getDatabase():
    db = get_db()
    information = db.execute('SELECT * FROM destination_mapping').fetchall()
    return information

def queryDatabase(value):
    db = get_db()
    information = db.execute(value).fetchall()
    return information

def getCDMNames():
    db = get_db()
    df = pd.read_sql_query('SELECT variable FROM destination_mapping', db)
    return df

def getDataframe():
    db = get_db()
    df = pd.read_sql_query('SELECT * FROM destination_mapping', db)
    return df