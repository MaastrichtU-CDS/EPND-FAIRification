from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from flaskr import useDataset, useCDM, useLinkdata
import pandas as pd
import numpy as np

bp = Blueprint("linkdatasets",__name__)

#Code to load the needed values for the main page
@bp.route('/', methods=('GET', 'POST'))
def linker():
    #if request.method == "POST":
        #print('abc')
        #post_url = request.form['delete']
        #post_test = request.form['delete']
        #print(post_url)
    links = useLinkdata.getDatabase()
    linksdf = useLinkdata.getDataframe()
    useLinkdata.test()

    testLinksData = useLinkdata.retrieveLinks()
    testLinksData = testLinksData.values.tolist()
    x = 0
    for listing in testLinksData:
        temp = listing[2]
        cdmName = temp.replace(temp[:7], '')
        testLinksData[x].append(cdmName)
        x = x + 1


    #Gets the needed values for the dataset dropdown
    datasetVariables = useDataset.getDatasetTry()
    datasetVariablesList = datasetVariables.values.tolist()

    #Gets the needed values for the CDM dropdown
    CDM = getCDM()
    CDM = CDM[~(CDM['variable'].isin(linksdf['cdmcolumn']))].reset_index(drop=True)
    cdmcol = list(CDM['variable'])

    
    return render_template("linkdatasets/linkdatasets.html", linktry2=testLinksData, datasetVariablesList=datasetVariablesList, links=links, cdmcolumns=cdmcol)
    #return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)

#Code for submitting new mappings
@bp.route('/submit-form', methods = ['GET', 'POST'])
def submitForm():
    selectValueData = request.form.get('columns')
    selectValueCDM = request.form.get('cdmcolumns')

    useLinkdata.newLink(selectValueData, selectValueCDM)
    useLinkdata.addLink(selectValueData, selectValueCDM)

    return redirect(url_for("linkdatasets.linker"))

#Code for deleting a mapping
@bp.route('/deletelink', methods=('POST',))
def deleteLink():
    value = request.form['delete']
    valueSplit = value.split(",")
    useLinkdata.delLink(valueSplit[0], valueSplit[1])
    #useLinkdata.deleteLink(value1)
    #useLinkdata.delLink(value1, value2)

    return redirect(url_for("linkdatasets.linker"))

def getCDM():
    #CDM = pd.read_csv("destination_mapping.csv")
    CDM = useCDM.getDataframe()
    CDM = CDM[['variable', 'values', 'type']]
    t1 = CDM['values'].notna()
    CDM['type'] = np.select([t1], ['cat'], CDM['type'])
    return CDM