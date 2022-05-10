import statistics
from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from flaskr import useDataset, useCDM, useLinkdata
import pandas as pd
import numpy as np

bp = Blueprint("linkdatasets",__name__)

#Code to load the needed values for the main page
@bp.route('/link', methods=('GET', 'POST'))
def linker():
    #Gets Mapping Links
    linksData = useLinkdata.retrieveMappings()
    linksDataList = linksData.values.tolist()

    #Gets the needed values for the dataset dropdown
    datasetVariables = useDataset.getDatasetUri()
    datasetVariables = datasetVariables[~(datasetVariables['colUri'].isin(linksData['columnUri']))].reset_index(drop=True)
    datasetVariablesList = datasetVariables.values.tolist()

    #CDM Old Way
    #CDM = getCDM()
    #CDM = CDM[~(CDM['variable'].isin(linksdf['cdmcolumn']))].reset_index(drop=True)
    #cdmcol = list(CDM['variable'])

    #Gets the needed values for the CDM dropdown
    cdm = useCDM.getCDMUri()
    cdmlist = cdm.values.tolist()

    for link in linksDataList:
        tempDF = useDataset.getData(link[3])
        tempDF.columns = {link[2]}
        try:
            rawData = pd.concat([rawData, tempDF], axis=1, join='inner')
        except:
            rawData = tempDF
    
    if "rawData" in locals():
        statisticsDataframe = rawData.describe(include='all')
    else:
        print(rawData)


    #useDataset.othertry(linksDataList)

    return render_template("linkdatasets/linkdatasets.html", cdmlist=cdmlist, links=linksDataList, datasetVariablesList=datasetVariablesList, tables=[statisticsDataframe.to_html(classes='data')], titles=statisticsDataframe.columns.values)
    #return render_template("linkdatasets/linkdatasets.html", links=links, columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)

#Code for submitting new mappings
@bp.route('/submit-form', methods = ['GET', 'POST'])
def submitForm():
    selectValueData = request.form.get('columns')
    selectValueCDM = request.form.get('cdmcolumns')

    useLinkdata.createLink(selectValueData, selectValueCDM)

    return redirect(url_for("linkdatasets.linker"))

#Code for deleting a mapping
@bp.route('/deletelink', methods=('POST',))
def deleteLink():
    value = request.form['delete']
    valueSplit = value.split(",")
    useLinkdata.deleteLink(valueSplit[0], valueSplit[1])

    return redirect(url_for("linkdatasets.linker"))

#def getCDM():
    #CDM = pd.read_csv("destination_mapping.csv")
    #CDM = useCDM.getDataframe()
    #CDM = CDM[['variable', 'values', 'type']]
    #t1 = CDM['values'].notna()
    #CDM['type'] = np.select([t1], ['cat'], CDM['type'])
    #return CDM