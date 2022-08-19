from importlib.metadata import metadata
from flask import (
    Blueprint, render_template, request
)
from flaskr.services import data_service, triplestore, cedar_service

bp = Blueprint("data_controller",__name__)
rdfStore = None
triplifierRestUri = None

def __get_data_service():
    return data_service.DataEndpoint(rdfStore)

def __get_cedar_service():
    return cedar_service.CedarEndpoint(rdfStore)


@bp.route('/upload', methods=['GET'])
def upload():
    metadataUri = request.args.get("metadataUri")
    metadataName = __get_cedar_service().get_instance_name_for_uri(metadataUri)
    navigationPath=[
        {"name": "cohorts", "url": "/metadata"},
        {"name": "cohort:" + metadataName, "url": "/metadata/instance?uri=" + metadataUri},
        {"name": "add", "url": None}
        ]
    return render_template('data/upload.html', metadataUri = metadataUri, triplifierRestUri=triplifierRestUri, navigationPath=navigationPath)

@bp.route('/upload/link', methods=['POST'])
def makeLink():
    cedarUri = request.form.get("metadataUri")
    taskId = request.form.get("taskId")
    dataUri = "http://data.local/" + taskId + "/"
    ontologyUri = "http://ontology.local/" + taskId + "/"
    __get_data_service().store_cedar_task_link(cedarUri, dataUri, ontologyUri, taskId)
    return "ok"