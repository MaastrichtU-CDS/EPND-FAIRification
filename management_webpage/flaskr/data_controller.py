from importlib.metadata import metadata
from flask import (
    Blueprint, render_template, request, redirect
)
from flaskr.services import data_service, triplestore, cedar_service
import requests

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
    errorMessage = request.args.get("error")
    metadataName = __get_cedar_service().get_instance_name_for_uri(metadataUri)
    navigationPath=[
        {"name": "cohorts", "url": "/metadata"},
        {"name": "cohort:" + metadataName, "url": "/metadata/instance?uri=" + metadataUri},
        {"name": "add", "url": None}
        ]
    return render_template('data/upload.html', metadataUri = metadataUri, navigationPath=navigationPath, errorMessage=errorMessage)

@bp.route("/upload", methods=['POST'])
def submit():
    fileObj = request.files.get("formFile")

    files = {
        'file': (fileObj.filename, fileObj.stream)
    }
    response = requests.post(triplifierRestUri + "/api/binary", files=files)
    
    if response.status_code >= 200 & response.status_code < 300:
        cedarUri = request.form.get("metadataUri")

        json_response = response.json()
        print(json_response["id"])

        make_link_cedar_and_file(cedarUri=cedarUri, taskId=json_response["id"])
        return redirect(f"/metadata/instance?uri={cedarUri}")
    
    return redirect(f"/metadata/instance?uri={cedarUri}&error=Could not upload file")

def make_link_cedar_and_file(cedarUri, taskId):
    dataUri = "http://data.local/" + taskId + "/"
    ontologyUri = "http://ontology.local/" + taskId + "/"
    __get_data_service().store_cedar_task_link(cedarUri, dataUri, ontologyUri, taskId)