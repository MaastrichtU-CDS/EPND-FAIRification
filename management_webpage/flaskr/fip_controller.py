from flask import (
    Blueprint, render_template, request, redirect, url_for
)
import validators

bp = Blueprint("fip_controller",__name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template("fip/index.html")

@bp.route('/', methods=['POST'])
def post_fip():
    fip_uri = request.form.get("fip-uri")
    if not validators.url(fip_uri):
        return render_template("fip/index.html", warning="Not a valid URI")
    return render_template("fip/index.html")