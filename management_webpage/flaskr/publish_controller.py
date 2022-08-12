from importlib.metadata import metadata
from flask import (
    Blueprint, render_template, request
)
from flaskr.services import data_service, triplestore
import logging

bp = Blueprint("publish_controller",__name__)
rdfStore = None
triplifierRestUri = None

def __get_data_service():
    return data_service.DataEndpoint(rdfStore)

@bp.route('/publish/preview', methods=['GET'])
def upload():
    metadataUri = request.args.get("metadataUri")
    dService = __get_data_service()

    ## Retrieve the shacl elements based on the metadata uri -> template -> fip -> shacl
    fipAndShacl = dService.get_fip_and_shacl_for_cedar_instance(metadataUri)
    shapesGraphUri = fipAndShacl[0]['shapesGraph']['value']

    ## Find the mapped columns based on the shacl file
    foundShapes = dService.get_mapped_shapes_from_shacl(shapesGraphUri)

    ## Generate the target table based on the mapped columns
    for foundShape in foundShapes:
        targetClass = foundShape['targetClass']['value']
        columnClass = foundShape['columnClass']['value']
        variableType = foundShape['variableType']['value']

        logging.debug(f"Processing target class {targetClass} with column {columnClass}")

        ## retrieve row URI and targetClass column value
        ## if variableType is categorical, map value to rdf:type

        ## Afterwards append/merge with existing DataFrame

    return render_template('publish/preview.html', metadataUri = metadataUri, previewTable=foundShapes)