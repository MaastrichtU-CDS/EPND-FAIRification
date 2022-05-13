from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app, Response
)
from flaskr.services import cedar_service, triplestore
import json
import requests
import uuid
from rdflib import Graph
import datetime
from tzlocal import get_localzone

bp = Blueprint("cedar_controller",__name__)
rdfStore = None
cedar_instance_base_url = "http://cedar.local/instances"

def __get_cedar_service():
    return cedar_service.CedarEndpoint(rdfStore)

@bp.route('/metadata', methods=['GET'])
def index():
    instances = __get_cedar_service().list_instances()
    # TODO: show the title of the template instance
    for idx, val in enumerate(instances):
        instances[idx]["instance"]["short"] = instances[idx]["instance"]["value"].replace(cedar_instance_base_url + "/", "")
    return render_template("cedar/index.html", instances=instances)

@bp.route("/metadata/add")
def cee():
    return render_template("cedar/add.html")

def get_template():
    cedar_location = __get_cedar_service().get_template_location()
    print(cedar_location)
    
    response = requests.get(cedar_location)
    template = response.json()
    return template

@bp.route("/api/cedar/template.json")
def template():
    """
    Retrieve cedar template from the main repository,
    and pass it to the embeddable editor in the front-end
    """
    template = get_template()
    return Response(json.dumps(template), mimetype='application/json')

@bp.route("/api/cedar/store", methods=["POST", "PUT"])
def store():
    """
    Function to store the actual data generated using the cedar embeddable editor.
    """
    template = get_template()
    session_id = uuid.uuid4()
    if request.method == "PUT":
        session_id = request.args.get("id")
    
    # fileNameJson = os.path.join(config['server']['storageFolder'], f"{session_id}.jsonld")
    # fileNameTurtle = os.path.join(config['server']['storageFolder'], f"{session_id}.ttl")

    local_tz = get_localzone()

    data_to_store = request.get_json()
    data_to_store = data_to_store["metadata"]
    data_to_store["schema:isBasedOn"] = template['@id']
    data_to_store["pav:createdOn"] = datetime.datetime.now(local_tz).isoformat()
    data_to_store["@id"] = f"{cedar_instance_base_url}/{session_id}"

    # with open(fileNameJson, "w") as f:
    #     json.dump(data_to_store, f, indent=4)
    
    g = Graph()
    g.parse(data=json.dumps(data_to_store), format='json-ld')
    # g.serialize(destination=fileNameTurtle)
    
    turtleData = g.serialize(format='nt')
    __get_cedar_service().store_instance(turtleData, data_to_store["@id"])

    return {"id": f"{session_id}", "message": "Hi there!"}