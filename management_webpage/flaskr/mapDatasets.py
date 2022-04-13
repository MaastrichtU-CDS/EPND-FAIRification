import statistics
from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from flaskr import useDataset, useCDM, useLinkdata
import pandas as pd
import numpy as np

bp = Blueprint("mapDatasets",__name__)

@bp.route('/mapping', methods=('GET', 'POST'))
def mapper():

    datasetColumns = useDataset.getDatasetUri()

    cdmColumns = useCDM.getCDMUri()

    linkedDatasets = useLinkdata.retrieveDatasetMapped()
    linkedDatasetsList = linkedDatasets.values.tolist()
    #print(linkedDatasetsList)
    #print(linkedDatasetsList[0][0])
    #if linkedDatasetsList[2][0]:
        #print('happy chicken')
    return render_template("mapdatasets/mapdatasets.html", mappings=linkedDatasetsList)



@bp.route('/detailedMapping', methods=('GET', 'POST'))
def detailedMapper():
    value = request.form['chosen']

    linkedDatasets = useLinkdata.retrieveDatasetMapped()

    cdmColumns= useCDM.getCDMUri()
    cdmColumnsList = cdmColumns.values.tolist()

    linkedInformationDataframe = linkedDatasets[linkedDatasets['columnUri'].str.contains(value)]
    linkedInformationList=linkedInformationDataframe.values.tolist()
    return render_template("mapdatasets/detailedMapping.html", chosenMapping=linkedInformationList, cdmValues = cdmColumnsList)

@bp.route('/commit', methods = ['GET', 'POST'])
def submitForm():
    selectedValue = request.form.get('cdmValues')    
    print('Values:')
    print(selectedValue)
    valueSplit = selectedValue.split(",")
    print('Split:')
    print(valueSplit)
    if valueSplit[1] == 'nan':
        print('Ja')
        useLinkdata.createLink(valueSplit[0], valueSplit[2])
    else:
        print('nee')
        useLinkdata.deleteLink(valueSplit[0], valueSplit[1])
        useLinkdata.createLink(valueSplit[0], valueSplit[2])

    #useLinkdata.createLink(selectValueData, selectValueCDM)
    return redirect(url_for("mapDatasets.mapper"))
    #return redirect(url_for("linkdatasets.linker"))