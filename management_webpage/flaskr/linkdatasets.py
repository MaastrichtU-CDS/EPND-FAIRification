from flask import (
    Blueprint, render_template, request
)
from flaskr import useDataset, useCDM, useLinkdata
import pandas as pd
import numpy as np

bp = Blueprint("linkdatasets",__name__,url_prefix="/linkdatasets")

@bp.route('/linkdatasets', methods=('GET', 'POST'))
def linker():
    useDataset.getTest()

    links = useLinkdata.getDatabase()
    linksdf = useLinkdata.getDataframe()

    dataset = getDatasetNames()
    dataset = dataset[~(dataset.isin(linksdf['datacolumn']))].reset_index(drop=True)
    datacol = dataset

    CDM = getCDM()
    CDM = CDM[~(CDM['variable'].isin(linksdf['cdmcolumn']))].reset_index(drop=True)
    cdmcol = list(CDM['variable'])
    
    return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol)
    #return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)

@bp.route('/submit-form', methods = ['GET', 'POST'])
def submitForm():
    selectValueData = request.form.get('columns')
    selectValueCDM = request.form.get('cdmcolumns')
    print(selectValueData)
    print(selectValueCDM)
    useLinkdata.newLink(selectValueData, selectValueCDM)

    links = useLinkdata.getDatabase()
    linksdf = useLinkdata.getDataframe()

    dataset = getDatasetNames()
    dataset = dataset[~(dataset.isin(linksdf['datacolumn']))].reset_index(drop=True)
    datacol = dataset

    CDM = getCDM()
    CDM = CDM[~(CDM['variable'].isin(linksdf['cdmcolumn']))].reset_index(drop=True)
    cdmcol = list(CDM['variable'])

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

def getDatasetNames():
    dataset = useDataset.getDatasetNames()
    return dataset

@bp.route('/<string:name>/deleteLink', methods=('POST',))
def deleteLink(name):
    useLinkdata.deleteLink(name)

    links = useLinkdata.getDatabase()
    linksdf = useLinkdata.getDataframe()

    dataset = getDatasetNames()
    dataset = dataset[~(dataset.isin(linksdf['datacolumn']))].reset_index(drop=True)
    datacol = dataset

    CDM = getCDM()
    CDM = CDM[~(CDM['variable'].isin(linksdf['cdmcolumn']))].reset_index(drop=True)
    cdmcol = list(CDM['variable'])


    return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol)
    #return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)
