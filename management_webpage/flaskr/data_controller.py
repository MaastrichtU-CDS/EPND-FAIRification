from flask import (
    Blueprint, render_template
)

bp = Blueprint("data_controller",__name__)


@bp.route('/upload', methods=['GET'])
def upload():
    return render_template('data/upload.html')