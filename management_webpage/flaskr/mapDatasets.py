import statistics
from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from flaskr import useDataset, useCDM, useLinkdata, statisticalMetadata
import pandas as pd
import numpy as np

bp = Blueprint("mapDatasets",__name__)

#Default homepage for the program
@bp.route('/mapping', methods=('GET', 'POST'))
def mapper():

    datasetColumns = useDataset.getDatasetUri()

    cdmColumns = useCDM.getCDMUri()
    #Gets all information of the linked data
    linkedDatasets = useLinkdata.retrieveDatasetMapped()
    linkedDatasetsList = linkedDatasets.values.tolist()

    #Renders the default template
    return render_template("mapdatasets/mapdatasets.html", mappings=linkedDatasetsList)


#Loads the template containing more information
@bp.route('/detailedMapping', methods=('GET', 'POST'))
def detailedMapper():
    #Gets the chosen mapping
    value = request.form['chosen']

    #Gets all mapped values
    linkedDatasets = useLinkdata.retrieveDatasetMapped()

    #Gets all CDM definitions
    cdmColumns= useCDM.getCDMUri()
    cdmColumnsList = cdmColumns.values.tolist()

    #Searches for the mapping that includes the chosen value
    linkedInformationDataframe = linkedDatasets[linkedDatasets['columnUri'].str.contains(value)]
    linkedInformationList=linkedInformationDataframe.values.tolist()

    linkedInformationDataframe['cdmUri'] = linkedInformationDataframe['cdmUri'].isnull()
    linkedInformationDataframe = linkedInformationDataframe.reset_index(drop=True)
    if linkedInformationDataframe['cdmUri'][0] == True:
        data = useDataset.getData(value)
        metadata = statisticalMetadata.numericMetadata(data)
    else:
        cdmTotal = useCDM.getCDMFull()
        cdmTotal = cdmTotal.loc[cdmTotal['variableUri'] == linkedInformationList[0][0]]
        cdmTotal = cdmTotal.reset_index(drop=True)
        data = useDataset.getData(value)
        if cdmTotal['variableType'][0] == 'http://semanticscience.org/resource/SIO_000914' or cdmTotal['variableType'][0] == 'http://semanticscience.org/resource/SIO_000137':
            metadata = statisticalMetadata.categoricalMetadata(data)
            metadata = metadata.to_frame()
        else:
            metadata = statisticalMetadata.numericMetadata(data)
        

    #Renders the detailedMapping template
    return render_template("mapdatasets/detailedMapping.html", metadata=metadata.to_html(), chosenMapping=linkedInformationList, cdmValues = cdmColumnsList)

#Adds a new mapping, or changes a existing mapping to a new one
@bp.route('/commit', methods = ['GET', 'POST'])
def submitForm():
    #Gets the selected values
    selectedValue = request.form.get('cdmValues')    
    valueSplit = selectedValue.split(",")
    if valueSplit[1] == 'nan':
        useLinkdata.createLink(valueSplit[0], valueSplit[2])
    else:
        useLinkdata.deleteLink(valueSplit[0], valueSplit[1])
        useLinkdata.createLink(valueSplit[0], valueSplit[2])

    #Renders the default template
    return redirect(url_for("mapDatasets.mapper"))

#Deletes a current mapping
@bp.route('/deletemapping', methods=('POST',))
def deleteMapping():
    #Gets the mapping that needs to be deleted, and deletes it
    value = request.form['delete']
    valueSplit = value.split(",")
    useLinkdata.deleteLink(valueSplit[0], valueSplit[1])

    #Renders the default template
    return redirect(url_for("mapDatasets.mapper"))