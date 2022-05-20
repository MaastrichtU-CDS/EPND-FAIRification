from importlib.metadata import metadata
from flask import (
    Blueprint, render_template, request
)
from flaskr.services import data_service, triplestore

bp = Blueprint("data_controller",__name__)
rdfStore = None
triplifierRestUri = None

def __get_data_service():
    return data_service.DataEndpoint(rdfStore)


@bp.route('/upload', methods=['GET'])
def upload():
    metadataUri = request.args.get("metadataUri")
    return render_template('data/upload.html', metadataUri = metadataUri, triplifierRestUri=triplifierRestUri)

@bp.route('/upload/link', methods=['POST'])
def makeLink():
    cedarUri = request.form.get("metadataUri")
    taskId = request.form.get("taskId")
    dataUri = "http://data.local/" + taskId + "/"
    ontologyUri = "http://ontology.local/" + taskId + "/"
    __get_data_service().store_cedar_task_link(cedarUri, dataUri, ontologyUri, taskId)
    return "ok"