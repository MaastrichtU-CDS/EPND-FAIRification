from flask import (
    Blueprint, render_template, request, redirect, url_for, current_app
)
import validators
from flaskr.services import fip_service, triplestore, nanopub_service
import rdflib
import re, os
from werkzeug.utils import secure_filename

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
    g = rdflib.Graph()
    fip = ""
    try:
        # Checking between raw ttl files and nanopub links
        if validators.url(fip_uri):
            if not fip_uri.endswith('.ttl', -4):
                np_service = nanopub_service.NanopubService(fip_uri)
                fip = np_service.parse_shacl_uri()
                g.parse(data=fip)
        else:
            g.parse(fip_uri, format='turtle')
    except Exception as e:
        raise Exception("Could not load the FIP file at %s - Is the URL\
                            correct?" % fip_uri)
    triples = g.serialize(format="turtle")
    fService = __get_fip_service()
    if not(validators.url(fip_uri)):
        fService.load_fip("http://local/" + fip_uri, triples)
    else:
        fService.load_fip(fip_uri, triples)
    fService.cache_shacl()

@bp.route('/', methods=['POST'])
def post_fip():
    if not request.files['fip-file'].filename == '':
        file = request.files['fip-file']
        file.save(secure_filename(file.filename))
        fip_uri = file.filename
        if not fip_uri:
            return render_template("fip/index.html", warning="Not a valid file")
    else:
        fip_uri = request.form.get("fip-uri")
        if not validators.url(fip_uri):
            return render_template("fip/index.html", warning="Not a valid URI")
    
    try:
        __parse_fip(fip_uri)
    except Exception as e:
        return render_template("fip/index.html", warning=e)

    return redirect(url_for("fip_controller.index"))
