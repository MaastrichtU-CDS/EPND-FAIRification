from importlib.metadata import metadata
from flask import (
    Blueprint, render_template, request
)
from flaskr.services import data_service, triplestore

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
    print(shapesGraphUri)

    ## Find the mapped columns based on the shacl file

    ## Generate the target table based on the mapped columns

    return render_template('publish/preview.html', metadataUri = metadataUri)