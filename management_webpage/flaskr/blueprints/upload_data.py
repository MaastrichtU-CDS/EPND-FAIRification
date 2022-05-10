from werkzeug.utils import secure_filename
from flask import Flask, jsonify

from werkzeug.datastructures import FileStorage

from flask import (
    Blueprint, render_template, request, redirect, url_for
)

bp = Blueprint("uploaddataset",__name__)


@bp.route('/upload', methods=['GET'])
def upload():
    return render_template('upload_data.html')


@bp.route('/uploader', methods=['POST'])
def upload_file():
    f = request.files['files']
    f.save(secure_filename(f.filename))
    return jsonify(message="File '" + f.filename + "' uploaded")