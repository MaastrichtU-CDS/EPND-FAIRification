import statistics
from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from flaskr import useDataset, useCDM, useLinkdata
import pandas as pd
import numpy as np

bp = Blueprint("mapDatasets",__name__)

@bp.route('/mapping', methods=('GET', 'POST'))
def mapper():

    datasetColumns = useDataset.getDatasetUri()

    cdmColumns = useCDM.getCDMUri()

    linkedDatasets = useLinkdata.retrieveDatasetMapped()
    linkedDatasetsList = linkedDatasets.values.tolist()
    print(linkedDatasetsList)
    print(linkedDatasetsList[0][0])
    if linkedDatasetsList[2][0]:
        print('happy chicken')
    return render_template("mapdatasets/mapdatasets.html", mappings=linkedDatasetsList)



@bp.route('/detailedMapping', methods=('GET', 'POST'))
def detailedMapper():
    value = request.form['delete']
    print(value)
    return render_template("mapdatasets/detailedMapping.html")
