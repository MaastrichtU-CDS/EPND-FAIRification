import statistics
from flask import (
    current_app, Blueprint, render_template, request, redirect, url_for, jsonify
)
from flaskr import useDataset, useCDM, useLinkdata, statisticalMetadata, getCategories
from flaskr.services.triplestore import GraphDBTripleStore
from flaskr.services import cedar_service, data_service, triplestore
import pandas as pd
import numpy as np
import math

bp = Blueprint("mapDatasets",__name__)

def createBreadCrumbBasic(datasetId: str, dataOntologyUri: str=None):
    cedar_uri = useDataset.get_cedar_template_for_dataset_uri(datasetId)
    graphDbStore = GraphDBTripleStore(current_app.config.get("graphdb_server"),
                    current_app.config.get("repository"),
                    create_if_not_exists=True)
    cService = cedar_service.CedarEndpoint(graphDbStore)
    cedar_name = cService.get_instance_name_for_uri(cedar_uri)

    mappingUrl = None
    if dataOntologyUri is not None:
        mappingUrl = f"/column_mappings?identifier={datasetId}&ontology={dataOntologyUri}"

    return [
        {"name": "cohorts", "url": "/metadata"}, 
        {"name": "cohort:" + cedar_name, "url": "/metadata/instance?uri=" + cedar_uri},
        {"name": "mapping", "url": mappingUrl}
        ]


@bp.route('/column_mappings', methods=('GET', 'POST'))
def mapper():

    #column_mappings?identifier=88480db6-1ef1-45aa-bbe1-a2285caf1bac&ontology=http://ontology.local/88480db6-1ef1-45aa-bbe1-a2285caf1bac/
    identifier = request.args.get("identifier")
    dataOntologyUri = request.args.get("ontology")
    navigationPath = None
    if identifier is not None:
        navigationPath = createBreadCrumbBasic(identifier, dataOntologyUri)

    cdmColumns = useCDM.getCDMUri()
    #Gets all information of the linked data
    linkedDatasets = useLinkdata.retrieveDatasetMapped(identifier)
    linkedDatasetsList = linkedDatasets.values.tolist()
    for row in linkedDatasetsList:
        if type(row[0]) != str and math.isnan(row[0]):
            row[0] = None
            row[1] = None

    #Renders the default template
    return render_template("mapDatasets/mapDatasets.html", mappings=linkedDatasetsList, navigationPath=navigationPath)


@bp.route('/api/mappings', methods=['POST'])
def jsonMapper():

    datasetColumns = useDataset.getDatasetUri()

    cdmColumns = useCDM.getCDMUri()
    #Gets all information of the linked data
    datasetId = request.json['identifier']
    linkedDatasets = useLinkdata.retrieveDatasetMapped(datasetId)
    linkedDatasetsList = linkedDatasets.values.tolist()
    mappings = []
    for row in linkedDatasetsList:
        if type(row[0]) != str and math.isnan(row[0]):
                row[0] = None
                row[1] = None
        mappings.append({ "columnName": row[2], "columnUri": row[3], "cdmUri": row[0], "cdmUriLabel": row[1] })

    return jsonify(mappings)

#Loads the template containing more information
@bp.route('/detailedMapping', methods=['GET', 'POST'])
def detailedMapper():
    # Gets the chosen mapping
    print("In detailed mapping...")
    toBeModified = False
    if request.form.get('modify'):
        toBeModified = True
    value = request.args.get('columnUri')
    datasetId = request.args.get("identifier")
    # Gets all mapped values
    linkedDatasets = useLinkdata.retrieveDatasetMapped(datasetId)
    # Gets all CDM definitions
    cdmColumns= useCDM.getCDMUri()
    cdmColumnsList = cdmColumns.values.tolist()

    # Searches for the mapping that includes the chosen value
    linkedInformationDataframe = linkedDatasets[linkedDatasets['columnUri'].str.contains(value)]
    linkedInformationList=linkedInformationDataframe.values.tolist()
    linkedInformationDataframe['cdmUri'] = linkedInformationDataframe['cdmUri'].isnull()
    linkedInformationDataframe = linkedInformationDataframe.reset_index(drop=True)
    if linkedInformationDataframe['cdmUri'][0]:
        data = useDataset.getData(value)
        metadata = statisticalMetadata.numericMetadata(data)
        categoricalData = False
    else:
        # Through the CDM URI, obtain cell mappings if any
        columnUri = linkedInformationList[0][0]
        mappedValues = useDataset.getMappedCell(columnUri, datasetId)

        cdmTotal = useCDM.getCDMFull()
        cdmTotal = cdmTotal.loc[cdmTotal['variableUri'] == linkedInformationList[0][0]]
        cdmTotal = cdmTotal.reset_index(drop=True)
        data = useDataset.getData(value)
        targetValues=getCategories.getClassCategories(str(linkedInformationList[0][0]))
        if cdmTotal['variableTypeLabel'][0] == 'category':
            # The condition used below previously seemed to be causing issues based on
            # initial analysis and hence using a new condition which seem to
            # work for most of the test cases. Further proofing required. Might
            # break sometime in the future.
            # if cdmTotal['variableType'][0] == 'http://semanticscience.org/resource/SIO_000914' or cdmTotal['variableType'][0] == 'http://semanticscience.org/resource/SIO_000137':
            metadata = statisticalMetadata.categoricalMetadata(data)
            # On obtaining the categories through statistical metadata function,
            # perform outer join on category values and creating a new
            # dataframe for easy display in the front end.
            new_metadata = mappedValues.merge(metadata, on='categoricalValue', how='outer')
            # metadata = metadata.to_frame()
            categoricalData = True
            new_metadata = new_metadata[['categoricalValue', 'cellMapping', 'cellValue']]
        else:
            categoricalData = False
            metadata = statisticalMetadata.numericMetadata(data)
    if categoricalData: 
        # Renders the detailedMapping template
        if toBeModified:
            return render_template("mapDatasets/detailedMappingToModify.html",
                    metadata=new_metadata, chosenMapping=linkedInformationList, cdmValues =
                    cdmColumnsList, categoricalCheck=bool(categoricalData),
                    targetValues=targetValues['categoryLabel'].values)
        else:
            return render_template("mapDatasets/detailedMapping.html",
                    metadata=new_metadata, chosenMapping=linkedInformationList, cdmValues =
                    cdmColumnsList, categoricalCheck=bool(categoricalData),
                    targetValues=targetValues['categoryLabel'].values)
    else:
        if toBeModified:
            return render_template("mapDatasets/detailedMappingToModify.html",
                    metadata=metadata.to_html(),
                    chosenMapping=linkedInformationList,
                    cdmValues=cdmColumnsList)
        else:
            return render_template("mapDatasets/detailedMapping.html",
                metadata=metadata.to_html(),
                chosenMapping=linkedInformationList, cdmValues=cdmColumnsList)

#Adds a new mapping, or changes a existing mapping to a new one
@bp.route('/commit', methods = ['GET', 'POST'])
def submitForm():
    #Gets the selected values
    selectedValue = request.form.get('cdmValues')    
    datasetId = request.args.get('identifier')
    columnUri = request.args.get('columnUri')
    ontology = columnUri.rsplit('/',0)[0] + '/'
    valueSplit = selectedValue.split(",")
    if valueSplit[1] == 'nan':
        useLinkdata.createLink(datasetId, valueSplit[0], valueSplit[2])
    else:
        useLinkdata.deleteLink(datasetId, valueSplit[0], valueSplit[1])
        targetClass = useDataset.getMappedCell(valueSplit[1], datasetId)
        for index, row in targetClass.iterrows():
            useLinkdata.deleteCellLinksNoInsert(row['cellClass'], valueSplit[1], row['categoricalValue'], datasetId)
        useLinkdata.createLink(datasetId, valueSplit[0], valueSplit[2])
    #Renders the default template
    return redirect(url_for("mapDatasets.mapper", identifier=datasetId,
                            ontology=ontology))

@bp.route('/cellMapping', methods= ['GET', 'POST'])
# Maps the cell values to the selected drop down value in the front end.
# Checks if the values are already mapped, if yes - deletes just the equivalent
# class for already mapped values and then inserts for the same node. This is
# to avoid reinsertion of all triples. During fresh mapping, createCellLinks
# method is used.
def cellMapping():
    targetValues = []
    for i in range(int(request.form.get('rowCount'))):
        targetValues.append(request.form.get('targetValues'+ str(i)))
    for i in range(len(targetValues)):
        # Obtaining all the necessary values for further processing. We obtain
        # the category value like "2.0" or "1.0", the old value which is
        # "Feminine gender" for example, new selected value like "Masculine
        # gender" and the column URI like
        # http://purl.bioontology.org/ontology/SNOMEDCT/365873007
        catValue, oldValue, newValue, cdmValue = targetValues[i].split(",")
        datasetId = request.args.get('identifier')
        print(f"Target values are {targetValues}")
        if oldValue == newValue:
            print("No change detected in mapping. Not doing anything")
            continue
        elif not newValue:
            if not oldValue.__eq__("nan"):
                print("Deleting older cell links")
                olderValue = getCategories.getCategoryCode(cdmValue, oldValue)
                useLinkdata.deleteCellLinksNoInsert(olderValue['categoryUri'].loc[0],\
                        cdmValue, catValue, datasetId)
            else:
                print("Detected empty selection as the target selection,\
                        can't really do anything.")
            continue
        else:
            # Obtain namespaces
            ns = GraphDBTripleStore(current_app.config.get("graphdb_server"),
                    current_app.config.get("repository"),
                    create_if_not_exists=True).fetch_namespaces()
            # Obtaining the base URI. Not using a regex.
            baseUri = findBaseUri(ns, cdmValue)
            # Changing from category code string value to obtaining the entire
            # URI as the BASE URI is not consistent across the ontology. For
            # APOE, the BASE URI varies whereas for gender it does not.
            selectedValue = getCategories.getCategoryCode(cdmValue, newValue)
            # Delete the existing links
            if oldValue != "nan":
                print(f"Change in mapping detected. Will delete and remap values \
                        for {targetValues[i]}")
                # The UI only displays the human readable category and not the code
                # to fetch the code for the mapped category
                olderValue = getCategories.getCategoryCode(cdmValue, oldValue)
                print(f"Remapping values from: {olderValue['categoryUri'].loc[0]}\
                        to {selectedValue['categoryUri'].loc[0]}")
                # As getCategoryCode method has been changed, the effect is
                # on delete cell link as well. So this method is changed as well.
                useLinkdata.deleteCellLinks(selectedValue['categoryUri'].loc[0],\
                        olderValue['categoryUri'].loc[0], cdmValue, catValue,\
                        datasetId)
            else:
                # Create new link
                print("No existing link detected, creating new ones. Yay.")
                # As getCategoryCoede method has been changed, the effect is on
                # create cell link as well, so this method is modified as well.
                useLinkdata.createCellLink(selectedValue['categoryUri'].loc[0],\
                                           cdmValue, catValue, datasetId)
    
    return redirect(url_for("mapDatasets.mapper", identifier=datasetId, ontology=request.args.get('ontology')))

def findBaseUri(ns, cdmValue):
    # The code below finds the baseUri for a given column mapping
    # doing that using fetched_namespaces which is list of dictionaries
    for i in ns:
        for key, val in i.items():
            if key == 'namespace':
                for key1, val1 in val.items():
                    if key1 == 'value' and (val1 in cdmValue):
                        baseUri = val1
    return baseUri


#Deletes a current mapping
@bp.route('/api/deletemapping', methods=['POST'])
def deleteMappingAPI():
    #Gets the mapping that needs to be deleted, and deletes it
    datasetUri = request.json['datasetUri']
    cdmUri = request.json['cdmUri']
    datasetId = request.json['identifier']
    useLinkdata.deleteLink(datasetId, cdmUri, datasetUri)
    targetClass = useDataset.getMappedCell(cdmUri, datasetId) 
    for index, row in targetClass.iterrows():
        useLinkdata.deleteCellLinksNoInsert(row['cellClass'], cdmUri,
                                            row['categoricalValue'], datasetId)
    #Renders the default template
    return jsonify(status="success")
