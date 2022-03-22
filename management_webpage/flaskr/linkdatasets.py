from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from flaskr import useDataset, useCDM, useLinkdata
import pandas as pd
import numpy as np

bp = Blueprint("linkdatasets",__name__)

@bp.route('/', methods=('GET', 'POST'))
def linker():
    links = useLinkdata.getDatabase()
    linksdf = useLinkdata.getDataframe()
    useLinkdata.test()
    #print(links)
    print(linksdf)

    dataset = getDatasetNames()
    dataset = dataset[~(dataset.isin(linksdf['datacolumn']))].reset_index(drop=True)
    datacol = dataset

    CDM = getCDM()
    CDM = CDM[~(CDM['variable'].isin(linksdf['cdmcolumn']))].reset_index(drop=True)
    cdmcol = list(CDM['variable'])
    
    return render_template("linkdatasets/linkdatasets.html", links=links, linksdf=[linksdf.to_html(classes='data')], columns=datacol, cdmcolumns=cdmcol)
    #return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)

@bp.route('/submit-form', methods = ['GET', 'POST'])
def submitForm():
    selectValueData = request.form.get('columns')
    selectValueCDM = request.form.get('cdmcolumns')

    useLinkdata.newLink(selectValueData, selectValueCDM)
    useLinkdata.addLink(selectValueData, selectValueCDM)

    return redirect(url_for("linkdatasets.linker"))

@bp.route('/<string:value1>/<string:value2>deleteLink', methods=('POST',))
def deleteLink(value1, value2):
    useLinkdata.deleteLink(value1)
    useLinkdata.delLink(value1, value2)

    return redirect(url_for("linkdatasets.linker"))

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