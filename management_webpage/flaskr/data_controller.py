from flask import (
    Blueprint, render_template, request
)
from flaskr.services import data_service, triplestore

bp = Blueprint("data_controller",__name__)
rdfStore = None

def __get_data_service():
    return data_service.DataEndpoint(rdfStore)


@bp.route('/upload', methods=['GET'])
def upload():
    metadataUri = request.args.get("metadataUri")
    return render_template('data/upload.html', metadataUri = metadataUri)

@bp.route('/upload/link', methods=['POST'])
def makeLink():
    cedarUri = request.form.get("metadataUri")
    taskId = request.form.get("taskId")
    taskUri = "http://data.local/dataset/" + taskId
    __get_data_service().store_cedar_task_link(cedarUri, taskUri)
    return "ok"