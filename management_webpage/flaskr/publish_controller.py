from importlib.metadata import metadata
from flask import (
    Blueprint, render_template, request
)
from flaskr.services import data_service, triplestore
import logging
from flaskr import useDataset

bp = Blueprint("publish_controller",__name__)
rdfStore = None
triplifierRestUri = None

def __get_data_service():
    return data_service.DataEndpoint(rdfStore)

@bp.route('/publish/preview', methods=['GET'])
def preview():
    metadataUri = request.args.get("metadataUri")
    dService = __get_data_service()

    ## Retrieve the shacl elements based on the metadata uri -> template -> fip -> shacl
    fipAndShacl = dService.get_fip_and_shacl_for_cedar_instance(metadataUri)
    shapesGraphUri = fipAndShacl[0]['shapesGraph']['value']

    ## Find the mapped columns based on the shacl file
    foundShapes = dService.get_mapped_shapes_from_shacl(shapesGraphUri)

    originalData = dService.get_data_for_column_class(foundShapes)

    ## Generate the target table based on the mapped columns

    for foundShape in foundShapes:
        if foundShape["variableType"] != "http://semanticscience.org/resource/SIO_000137":
            continue

        logging.debug(foundShape)
        targetClass = foundShape['targetClass']
        mappings = dService.get_mappings_for_target_class(targetClass)
        logging.debug("====================================")
        logging.debug("mappings:")
        logging.debug(mappings)
        
        ## add columns for mapped rows
        for row in originalData:
            rowName = foundShape['columnName']
            foundValue = row[rowName]

            for mapping in mappings:
                if mapping["categoricalValue"]==foundValue:
                    foundCellClass = mapping['cellClass']
                    foundCellClassShort = mapping['cellClass_short']
                    foundCellClassLabel = mapping['cellLabel']
                    break
                else:
                    foundCellClass = ""
                    foundCellClassShort = ""
                    foundCellClassLabel = ""

            row[rowName + "_class"] = foundCellClass
            row[rowName + "_classShort"] = foundCellClassShort
            row[rowName + "_classLabel"] = foundCellClassLabel

    return render_template('publish/preview.html', metadataUri = metadataUri, previewTable=originalData, foundShapes=foundShapes)