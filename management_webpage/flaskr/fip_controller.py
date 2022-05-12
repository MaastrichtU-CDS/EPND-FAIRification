from flask import (
    Blueprint, render_template, request, redirect, url_for
)

bp = Blueprint("fip_controller",__name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template("fip/index.html")

@bp.route('/', methods=['POST'])
def post_fip():
    print(request.form.get("fip-uri"))
    return render_template("fip/index.html")