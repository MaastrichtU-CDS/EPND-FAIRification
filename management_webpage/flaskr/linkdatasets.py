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
    df2 = useCDM.getDataframe()
    df3 = useLinkdata.getDataframe()

    #a = datacol.difference(df3.datacolumn)
    #df1_notin2 = df1[~(df1.isin(df2['variable']))].reset_index(drop=True)
    df_1notin3 = df1[~(df1.isin(df3['datacolumn']))].reset_index(drop=True)
    #df_1notin3 = df3[~(df3['datacolumn'].isin(df1))].reset_index(drop=True)
    df_2notin3 = df2[~(df2['variable'].isin(df3['cdmcolumn']))].reset_index(drop=True)
    #df_1notin3 = datacol[~(datacol.isin(df3['cdmcolumn']))].reset_index(drop=True)
    print(df_1notin3)
    print("tussen1")
    print(df1)
    #print("tussen2")
    #print(df1_notin2)
    #print("tussen3")
    #print(df1)

    #print("CDM")
    #print(df2["variable"][28])
    #print(df3["cdmcolumn"][5])
    #print('dataset')
    #print(df1[5])
    #print(df3["datacolumn"][6])

    
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
    print(selectValueData)
    print(selectValueCDM)
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

@bp.route('/<string:name>/deleteLink', methods=('POST',))
def deleteLink(name):
    useLinkdata.deleteLink(name)

    CDM = getCDM()
    cdmcol = list(CDM['variable'])

    dataset = getDataset()
    datacol = list(dataset.columns.values)

    links = useLinkdata.getDatabase()

    return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol)
    #return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)
