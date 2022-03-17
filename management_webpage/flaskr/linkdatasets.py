from flask import (
    Blueprint, render_template, request
)

from flaskr.db import get_db
from flaskr import useDataset, useCDM, useLinkdata
import pandas as pd
import numpy as np

bp = Blueprint("linkdatasets",__name__,url_prefix="/linkdatasets")





@bp.route('/linkdatasets', methods=('GET', 'POST'))
def linker():
    CDM = getCDM()
    cdmcol = list(CDM['variable'])

    dataset = getDataset()
    datacol = list(dataset.columns.values)

    links = useLinkdata.getDatabase()

    df1 = useDataset.getDatasetNames()
    df2 = useCDM.getCDMNames()
    df3 = useLinkdata.getDataframe()

    print(df1)
    print("space 1")
    print(df2)
    print("space 2")
    print(df3)
    #print("space 3")
    #print(df4)
    
    return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol)
    #return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)

@bp.route('/submit-form', methods = ['GET', 'POST'])
def submitForm():
    CDM = getCDM()
    cdmcol = list(CDM['variable'])

    dataset = getDataset()
    datacol = list(dataset.columns.values)

    selectValueData = request.form.get('columns')
    selectValueCDM = request.form.get('cdmcolumns')
    useLinkdata.newLink(selectValueData, selectValueCDM)
    links = useLinkdata.getDatabase()

    return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol)
    #return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)

def getCDM():
    #CDM = pd.read_csv("destination_mapping.csv")
    CDM = useCDM.getDataframe()
    CDM = CDM[['variable', 'values', 'type']]
    t1 = CDM['values'].notna()
    CDM['type'] = np.select([t1], ['cat'], CDM['type'])
    return CDM

def getDataset():
    dataset = useDataset.getDataframe()
    return dataset
    