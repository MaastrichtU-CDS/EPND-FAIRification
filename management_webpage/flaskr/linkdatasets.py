from flask import (
    Blueprint, render_template, request
)

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

bp = Blueprint("linkdatasets",__name__,url_prefix="/linkdatasets")
dataset = pd.read_csv("dataset.csv")
datadescribe = dataset.describe()
datacol = list(dataset.columns.values)

CDM = pd.read_csv("destination_mapping.csv")
CDM = CDM[['variable', 'values', 'type']]
t1 = CDM['values'].notna()
CDM['type'] = np.select([t1], ['cat'], CDM['type'])
cdmcol = list(CDM['variable'])

#dValue = dataset[['id']]
#plt.plot(idValue)
#plt.savefig('/new_plot.png')

@bp.route('/linkdatasets', methods=('GET', 'POST'))
def linker():
    return render_template("linkdatasets/linkdatasets.html", columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)
    #return render_template("linkdatasets/linkdatasets.html", name = 'new_plot', url='/new_plot.png', columns=datacol, cdmcolumns=cdmcol, CDMtables=[CDM.to_html(classes='data')], CDMtitles=CDM.columns.values, tables=[datadescribe.to_html(classes='data')], titles=datadescribe.columns.values)