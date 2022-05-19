import statistics
from flask import (
    current_app, Blueprint, render_template, request, redirect, url_for, jsonify
)
from flaskr import useDataset, useCDM, useLinkdata, statisticalMetadata, getCategories
from flaskr.services.triplestore import GraphDBTripleStore
import pandas as pd
import numpy as np
import math

bp = Blueprint("mapDatasets",__name__)

#Default homepage for the program
@bp.route('/', methods=('GET', 'POST'))
def mapper():

    datasetColumns = useDataset.getDatasetUri()

    cdmColumns = useCDM.getCDMUri()
    #Gets all information of the linked data
    linkedDatasets = useLinkdata.retrieveDatasetMapped()
    linkedDatasetsList = linkedDatasets.values.tolist()
    for row in linkedDatasetsList:
        if type(row[0]) != str and math.isnan(row[0]):
            row[0] = None
            row[1] = None

    #Renders the default template
    return render_template("mapDatasets/mapDatasets.html", mappings=linkedDatasetsList)


@bp.route('/api/mappings', methods=['GET'])
def jsonMapper():

    datasetColumns = useDataset.getDatasetUri()

    cdmColumns = useCDM.getCDMUri()
    #Gets all information of the linked data
    linkedDatasets = useLinkdata.retrieveDatasetMapped()
    linkedDatasetsList = linkedDatasets.values.tolist()
    mappings = []
    for row in linkedDatasetsList:
        if type(row[0]) != str and math.isnan(row[0]):
                row[0] = None
                row[1] = None
        mappings.append({ "columnName": row[2], "columnUri": row[3], "cdmUri": row[0], "cdmUriLabel": row[1] })

    return jsonify(mappings)

#Loads the template containing more information
@bp.route('/detailedMapping', methods=['GET'])
def detailedMapper():
    #Gets the chosen mapping
    value = request.args.get('columnUri')

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
        categoricalData = False
    else:
        cdmTotal = useCDM.getCDMFull()
        cdmTotal = cdmTotal.loc[cdmTotal['variableUri'] == linkedInformationList[0][0]]
        cdmTotal = cdmTotal.reset_index(drop=True)
        data = useDataset.getData(value)
        categoricalData = True
        targetValues=getCategories.getClassCategories(str(linkedInformationList[0][0]))
        if cdmTotal['variableType'][0] == 'http://semanticscience.org/resource/SIO_000914' or cdmTotal['variableType'][0] == 'http://semanticscience.org/resource/SIO_000137':
            metadata = statisticalMetadata.categoricalMetadata(data)
            #metadata = metadata.to_frame()
        else:
            metadata = statisticalMetadata.numericMetadata(data)
    if categoricalData: 
        #Renders the detailedMapping template
        return render_template("mapDatasets/detailedMapping.html", metadata=metadata, titles=metadata.columns.values, chosenMapping=linkedInformationList, cdmValues = cdmColumnsList, categoricalCheck=bool(categoricalData), targetValues=targetValues['categoryLabel'].values)
    else:
        return render_template("mapDatasets/detailedMapping.html",
                metadata=metadata.to_html(),
                chosenMapping=linkedInformationList, cdmValues=cdmColumnsList)
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

@bp.route('/cellMapping', methods= ['GET', 'POST'])
#This is just a temporary method for dealing with cell value mapping on the
#front end and needs to be reworked. All sparql results are in dataframe form
#and the code is agnostic. It's primarily for dealing with this use case.
#Big TODO is there is only insertion at the moment, not checking if it's
#already mapped. If it is already mapped, deletion also is required.
def submitCellMapping():
    selectedValue = request.form.get('targetValues')
    superClass = request.form.get('getCdmValue')
    sourceValue = request.form.get('sourceValue')
    endpoint = current_app.config.get("rdf_endpoint")
    ns = GraphDBTripleStore(endpoint).fetch_namespaces()

    #need to find the baseUri for a given column mapping
    #doing that using fetched_namespaces which is list of dictionaries
    for i in ns:
        for key, val in i.items():
            if key == 'namespace':
                for key1, val1 in val.items():
                    if key1 == 'value' and (val1 in superClass):
                        baseUri = val1
    #The UI only displays the human readable category and not the code
    #to fetch the code for the mapped category
    selectedValue = getCategories.getCategoryCode(superClass, baseUri, selectedValue)
    useLinkdata.createCellLink(baseUri, selectedValue['category'].loc[0], superClass, sourceValue)
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

    #Deletes a current mapping
@bp.route('/api/deletemapping', methods=['POST'])
def deleteMappingAPI():
    #Gets the mapping that needs to be deleted, and deletes it
    datasetUri = request.json['datasetUri']
    cdmUri = request.json['cdmUri']
    useLinkdata.deleteLink(datasetUri, cdmUri)

    #Renders the default template
    return jsonify(status="success")
