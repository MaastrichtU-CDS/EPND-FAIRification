from flask import (
    Blueprint, render_template, request
)

from flaskr.db import get_db

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

bp = Blueprint("linkdatasets",__name__,url_prefix="/linkdatasets")
dataset = pd.read_csv("dataset.csv")
datadescribe = dataset.describe()
datacol = list(dataset.columns.values)

CDM = pd.read_csv("destination_mapping.csv")
CDM = CDM[['variable', 'values', 'type']]
t1 = CDM['values'].notna()
CDM['type'] = np.select([t1], ['cat'], CDM['type'])
cdmcol = list(CDM['variable'])

linkedData = pd.DataFrame({'Dataset': ['1'], 'CDM': ['2']})

@bp.route('/linkdatasets', methods=('GET', 'POST'))
def linker():
    db = get_db()
    links = db.execute('SELECT * FROM linkedTable').fetchall()
    return render_template("linkdatasets/linkdatasets.html", links=links, linkeddataTables=[linkedData.to_html(classes='linkeddata')], linkeddataTitles=linkedData.columns.values ,columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)

@bp.route('/submit-form', methods = ['GET', 'POST'])
def submitForm():
    selectValueData = request.form.get('columns')
    selectValueCDM = request.form.get('cdmcolumns')
    db = get_db()
    try:
        db.execute(
            "INSERT INTO linkedTable (datacolumn, cdmcolumn) VALUES (?, ?)",
            (selectValueData, selectValueCDM),
        )
        db.commit()
    except:
        pass
    links = db.execute('SELECT * FROM linkedTable').fetchall()

    return render_template("linkdatasets/linkdatasets.html", links=links, linkeddatatables=[linkedData.to_html(classes='linkeddata')], linkeddatatitles=linkedData.columns.values, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)


def get_post():
    post = get_db().execute(
        
    ).fetchone()

    return post