from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app, Response
)
import validators
from flaskr.services import cedar_service, triplestore
import rdflib
import json
import requests

bp = Blueprint("cedar_controller",__name__)
rdfStore = None

def __get_cedar_service():
    return cedar_service.CedarEndpoint(rdfStore)

@bp.route('/metadata', methods=['GET'])
def index():
    instances = __get_cedar_service().list_instances()
    print(instances)
    # for idx, val in enumerate(instances):
    #     instances[idx]["instance"]["short"] = instances[idx]["instance"]["value"].replace(config["template"]["instance_base_url"] + "/", "")
    return render_template("cedar/index.html", instances=instances)

@bp.route("/metadata/add")
def cee():
    return render_template("cedar/add.html")

def get_template():
    cedar_location = __get_cedar_service().get_template_location()
    print(cedar_location)
    
    ## todo: use requests library
    response = requests.get(cedar_location)
    template = response.json()
    # template = json.loads(response.data)
    return template

@bp.route("/api/cedar/template.json")
def template():
    """
    Retrieve cedar template from the main repository,
    and pass it to the embeddable editor in the front-end
    """
    template = get_template()
    return Response(json.dumps(template), mimetype='application/json')