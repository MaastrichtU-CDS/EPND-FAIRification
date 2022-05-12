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

@bp.route('/', methods=['GET'])
def index():
    return render_template("fip/index.html")

@bp.route('/', methods=['POST'])
def post_fip():
    fip_uri = request.form.get("fip-uri")
    if not validators.url(fip_uri):
        return render_template("fip/index.html", warning="Not a valid URI")
    
    try:
        g = rdflib.Graph()
        g.parse(fip_uri, format="turtle")
    except:
        return render_template("fip/index.html", warning="Could not load the FIP file at %s - Is the URL correct?" % fip_uri)
    
    triples = g.serialize(format="nt")

    fService = __get_fip_service()
    fService.load_fip(fip_uri, triples)

    return redirect(url_for("fip_controller.index"))