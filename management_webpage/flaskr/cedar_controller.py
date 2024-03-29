from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app, Response
)
from flaskr.services import cedar_service, data_service, triplestore
import json
import requests
import uuid
from rdflib import Graph
import datetime
from tzlocal import get_localzone
import os

bp = Blueprint("cedar_controller",__name__)
rdfStore = None
cedar_instance_base_url = "http://cedar.local/instances"
turtle_folder = None

def __get_cedar_service():
    return cedar_service.CedarEndpoint(rdfStore)

def __get_data_service():
    return data_service.DataEndpoint(rdfStore)

@bp.route('/metadata', methods=['GET'])
def index():
    instances = __get_cedar_service().list_instances()
    for idx, val in enumerate(instances):
        print(instances[idx])
        instances[idx]["instance"]["short"] = instances[idx]["instance"]["value"].replace(cedar_instance_base_url + "/", "")
        if "label" in instances[idx]:
            if instances[idx]["label"]["value"] is not None:
                instances[idx]["instance"]["short"] = instances[idx]["label"]["value"]
    return render_template("cedar/index.html", instances=instances, navigationPath=[{"name": "cohorts", "url": "/metadata"}])

@bp.route("/metadata/add")
def cee():
    return render_template("cedar/add.html", navigationPath=[{"name": "cohorts", "url": "/metadata"}, {"name": "add", "url": None}])

@bp.route("/metadata/instance")
def showInstance():
    identifier = request.args.get("uri")
    properties = __get_cedar_service().describe_instance(identifier)
    references = __get_cedar_service().get_instance_links(identifier)

    distributionList = __get_data_service().get_distributions_for_metadata(identifier)
    for distribution in distributionList:
        distribution["tableNames"] = __get_data_service().get_tables_for_distribution(distribution["ontologyUri"]['value'])

    instanceTitle = __get_cedar_service().get_instance_name_for_uri(identifier)
    
    return render_template("cedar/instance.html", properties=properties, references=references, instance_uri=identifier, distributionList=distributionList, navigationPath=[{"name": "cohorts", "url": "/metadata"}, {"name": "cohort:" + instanceTitle, "url": None}])

@bp.route("/metadata/delete")
def delete_instance():
    identifier = request.args.get("uri")
    __get_cedar_service().drop_instance(identifier)
    return redirect(url_for("cedar_controller.index"))

def get_template():
    cedar_location = __get_cedar_service().get_template_location()
    print(cedar_location)

    if ("://localhost" in cedar_location) & (turtle_folder is not None):
        split_url = cedar_location.split("/")
        filename = split_url[len(split_url)-1]
        file_path = os.path.join(turtle_folder, filename)
        with open(file_path) as f:
            return json.load(f)
    else :
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

    local_tz = get_localzone()

    data_to_store = request.get_json()
    data_to_store = data_to_store["metadata"]
    data_to_store["schema:isBasedOn"] = template['@id']
    data_to_store["pav:createdOn"] = datetime.datetime.now(local_tz).isoformat()
    data_to_store["@id"] = f"{cedar_instance_base_url}/{session_id}"
    
    g = Graph()
    g.parse(data=json.dumps(data_to_store), format='json-ld')
    turtleData = g.serialize(format='nt')
    __get_cedar_service().store_instance(turtleData, data_to_store["@id"])

    return {"id": f"{session_id}", "message": "Hi there!"}
