from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app
)
import validators
from flaskr.services import cedar_service, triplestore
import rdflib

bp = Blueprint("cedar_controller",__name__)
rdfStore = None

def __get_fip_service():
    return cedar_service.CedarEndpoint(rdfStore)

@bp.route('/metadata', methods=['GET'])
def index():
    instances = __get_fip_service().list_instances()
    print(instances)
    # for idx, val in enumerate(instances):
    #     instances[idx]["instance"]["short"] = instances[idx]["instance"]["value"].replace(config["template"]["instance_base_url"] + "/", "")
    return render_template("cedar/index.html", instances=instances)