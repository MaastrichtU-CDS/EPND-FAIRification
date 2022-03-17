from flaskr.db import get_db
import pandas as pd

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