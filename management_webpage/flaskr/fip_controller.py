from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app
)
import validators
from flaskr.services import fip_service, triplestore
import rdflib

bp = Blueprint("fip_controller",__name__)
rdfStore = None

def __get_fip_service():
    return fip_service.FipService(rdfStore)

def __visualizeFip(foundFips):
    return render_template("fip/inform.html", foundFips=foundFips)

@bp.route('/', methods=['GET'])
def index():

    fService = __get_fip_service()
    foundFips = fService.get_fip()
    if len(foundFips) > 0:
        return __visualizeFip(foundFips)

    return render_template("fip/index.html")

def __parse_fip(fip_uri):
    try:
        g = rdflib.Graph()
        g.parse(fip_uri, format="turtle")
    except Exception as e:
        raise Exception("Could not load the FIP file at %s - Is the URL correct?" % fip_uri)
    
    triples = g.serialize(format="turtle")

    fService = __get_fip_service()
    fService.load_fip(fip_uri, triples)
    fService.cache_shacl()

@bp.route('/', methods=['POST'])
def post_fip():
    fip_uri = request.form.get("fip-uri")
    if not validators.url(fip_uri):
        return render_template("fip/index.html", warning="Not a valid URI")
    
    try:
        __parse_fip(fip_uri)
    except Exception as e:
        return render_template("fip/index.html", warning=e)

    return redirect(url_for("fip_controller.index"))