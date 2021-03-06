import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests
from io import StringIO
import time

queryT = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?tstage
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100029 ?neoplasm.
        ?neoplasm roo:P100244 ?tstagev.
        ?tstagev dbo:has_cell ?cell.
        ?cell a ?t.
        FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732"))
        BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?tstage)
    }
    }
            """

queryG = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?gender
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100018 ?genderv.
        ?genderv dbo:has_cell ?cell.
        ?cell a ?g.
        FILTER regex(str(?g), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197"))
        BIND(strafter(str(?g), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?gender)
    }
}
"""
queryN = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?nstage
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100029 ?neoplasm.
        ?neoplasm roo:P100242 ?nstagev.
        ?nstagev dbo:has_cell ?cell.
        ?cell a ?n.
        FILTER regex(str(?n), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714"))
        BIND(strafter(str(?n), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?nstage)
    }
    }
"""
queryM = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?mstage
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100029 ?neoplasm.
        ?neoplasm roo:P100241 ?mstagev.
        ?mstagev dbo:has_cell ?cell.
        ?cell a ?m.
        FILTER regex(str(?m), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700"))
        BIND(strafter(str(?m), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?mstage)
    }
    }
"""
queryS = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?survival
    WHERE {
    OPTIONAL
    {
        ?tablerow roo:P100254 ?survivalv.
        ?survivalv dbo:has_cell ?cell.
        ?cell a ?s.
        FILTER regex(str(?s), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987"))
        BIND(strafter(str(?s), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?survival)
    }
    }
"""
queryAge = """
	PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?agevalue   
    WHERE 
        {
        ?tablerow roo:hasage ?age.
        ?age dbo:has_cell ?cell.
        ?cell roo:P100042 ?agevalue.  
	}
"""
queryAjccSex = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?Gender ?AJCC ?TumourLocation
    WHERE {
    ?tablerow roo:P100018 ?genderv.
    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100219 ?ajccv.
    ?neoplasm roo:P100202 ?tumourv.

    ?genderv dbo:has_cell ?gendercell.
    ?ajccv dbo:has_cell ?ajcccell.
    ?tumourv dbo:has_cell ?tumourcell.

    ?gendercell a ?g.
    ?ajcccell a ?a.
    ?tumourcell a ?t.

    FILTER regex(str(?g), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197"))
    FILTER regex(str(?a), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971"))
    FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423"))

    BIND(strafter(str(?g), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?Gender)
    BIND(strafter(str(?a), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?AJCC)
    BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?TumourLocation)
}
"""
queryAjcc = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?ajcc
    WHERE {
    OPTIONAL {
    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100219 ?ajccv.
    ?ajccv dbo:has_cell ?ajcccell.
    ?ajcccell a ?a.
    FILTER regex(str(?a), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27966|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28054|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27970|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C27971"))
    BIND(strafter(str(?a), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?ajcc)   
    } 
}
"""
queryTumour = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?TumourLocation
    WHERE {
    OPTIONAL {
    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100202 ?tumour. 
    ?tumour dbo:has_cell ?tumourcell. 
    ?tumourcell a ?t.
    FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12762|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12246|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12420|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C12423"))
    BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?TumourLocation)
    }
}
"""
queryHpv = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?hpv
    WHERE {
    OPTIONAL {
    ?tablerow roo:P100022 ?hpvv.
    ?hpvv dbo:has_cell ?hpvcell.
    ?hpvcell a ?h.
    FILTER regex(str(?h), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C128839|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C131488"))
    BIND(strafter(str(?h), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?hpv)
   }
}
"""
queryChemo = """
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?therapy
    WHERE {
    OPTIONAL {
    ?tablerow roo:P100231 ?chemov.
    ?chemov dbo:has_cell ?chemocell.
    ?chemocell a ?c.
    FILTER regex(str(?c), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C94626|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C15313"))
    BIND(strafter(str(?c), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?therapy)
   }
}
"""
def queryresult(repo, query):
    endpoint = "http://rdf-store:7200/repositories/" + repo
    annotationResponse = requests.post(endpoint,
                                       data="query=" + query,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.text
    return output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.H5("Dataset:"),
    dcc.Checklist(
        id='dataset',
        options=[
            {'label': 'HNSCC', 'value': 'hnscc'},
            {'label': 'HN_ONE', 'value': 'hn_one'},
            {'label': 'OPC', 'value': 'opc'},
            {'label': 'HEAD_NECK', 'value': 'head_neck'}
        ],
        value=['hn_one'],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Loading(
        id="loading-2",
        children=[html.Div([html.Div(id="loading-output-2")])],
        type="default"
    ),
    html.Div(children=[
        dcc.Graph(id="sunburst", style={"width": 800, "margin": 0, 'display': 'inline-block'}),
        dcc.Graph(id="scatter", style={"width": 400, "margin": 0, 'display': 'inline-block'}),
        #dcc.Graph(id="box"),
    ]),
    html.Div([
        html.H5("Choose an option:"),
        dcc.Dropdown(
            id='columns',
            value='gender',
            options=[{'label': 'Gender', 'value': 'gender'},
                     {'label': 'T stage', 'value': 'tstage'},
                     {'label': 'N stage', 'value': 'nstage'},
                     {'label': 'M stage', 'value': 'mstage'},
                     {'label': 'Survival Status', 'value': 'survival'},
                     {'label': 'HPV Status', 'value': 'hpv'},
                     {'label': 'AJCC Stage', 'value': 'ajcc'},
                     {'label': 'Tumour Location', 'value': 'TumourLocation'},
                     {'label': 'Therapy given', 'value': 'therapy'}, ],
            clearable=False,
            style={'width': '220px'}),
        html.Div(children=[
            dcc.Graph(id="pie-chart")]),

    ])
])

result_hnscc = pd.DataFrame()
result_hn_one = pd.DataFrame()
result_hn = pd.DataFrame()
result_opc = pd.DataFrame()
codedict = {
        "C16576": "Female", "C20197": "Male", "C27966": "Stage I", "C28054": "Stage II",
        "C27970": "Stage III", "C27971": "Stage IV", "C12762": "Oropharynx", "C12420": "Larynx",
        "C12246": "Hypopharynx", "C12423": "Nasopharynx", "C48719": "T0", "C48720": "T1", "C48724": "T2",
        "C48728": "T3", "C48732": "T4", "C48705": "N0", "C48706": "N1", "C48786": "N2", "C48714": "N3",
        "C48699": "M0", "C48700": "M1", "C28554": "Dead", "C37987": "Alive", "C128839": "HPV Positive",
        "C131488": "HPV Negative", "C94626": "ChemoRadiotherapy", "C15313": "Radiotherapy"
    }
querylists = [queryT, queryG, queryN, queryM, queryS,
              queryAjcc, queryTumour, queryHpv, queryChemo]
for lists in querylists:
    result_data_hnscc = queryresult('hnscc', lists)
    data_hnscc = pd.read_csv(StringIO(result_data_hnscc))
    result_hnscc = pd.concat([result_hnscc, data_hnscc], axis=1)
    for col in result_hnscc.columns:
        result_hnscc[col] = result_hnscc[col].map(codedict).fillna(result_hnscc[col])
for lists in querylists:
    result_data_hn_one = queryresult('hn_one', lists)
    data_hn_one = pd.read_csv(StringIO(result_data_hn_one))
    result_hn_one = pd.concat([result_hn_one, data_hn_one], axis=1)
    for col in result_hn_one.columns:
        result_hn_one[col] = result_hn_one[col].map(codedict).fillna(result_hn_one[col])
for lists in querylists:
    result_data_hn = queryresult('head_neck', lists)
    data_hn = pd.read_csv(StringIO(result_data_hn))
    result_hn = pd.concat([result_hn, data_hn], axis=1)
    for col in result_hn.columns:
        result_hn[col] = result_hn[col].map(codedict).fillna(result_hn[col])
for lists in querylists:
    result_data_opc = queryresult('opc', lists)
    data_opc = pd.read_csv(StringIO(result_data_opc))
    result_opc = pd.concat([result_opc, data_opc], axis=1)
    for col in result_opc.columns:
        result_opc[col] = result_opc[col].map(codedict).fillna(result_opc[col])

datalist = {'hnscc', 'hn_one', 'head_neck', 'opc'}
for lists in datalist:
    if lists == "hnscc":
        result_data = queryresult('hnscc', queryAjccSex)
        hnscc = pd.read_csv(StringIO(result_data))
        for col in hnscc.columns:
            hnscc[col] = hnscc[col].map(codedict).fillna(hnscc[col])
    if lists == "hn_one":
        result_data = queryresult('hn_one', queryAjccSex)
        hn_one = pd.read_csv(StringIO(result_data))
        for col in hn_one.columns:
            hn_one[col] = hn_one[col].map(codedict).fillna(hn_one[col])
    if lists == "head_neck":
        result_data = queryresult('head_neck', queryAjccSex)
        head_neck = pd.read_csv(StringIO(result_data))
        for col in head_neck.columns:
            head_neck[col] = head_neck[col].map(codedict).fillna(head_neck[col])
    if lists == "opc":
        result_data = queryresult('opc', queryAjccSex)
        opc = pd.read_csv(StringIO(result_data))
        for col in opc.columns:
            opc[col] = opc[col].map(codedict).fillna(opc[col])

result1 = queryresult('hnscc', queryAge)
result_age_hnscc = pd.read_csv(StringIO(result1))

result2 = queryresult('hn_one', queryAge)
result_age_hn_one = pd.read_csv(StringIO(result2))

result3 = queryresult('head_neck', queryAge)
result_age_hn = pd.read_csv(StringIO(result3))

result4 = queryresult('opc', queryAge)
result_age_opc = pd.read_csv(StringIO(result4))

@app.callback(
    Output("sunburst", "figure"),
    [Input("dataset", "value"),
     Input("columns", "value")])
def update_sun(dataset, columns):
    result = pd.DataFrame()
    if dataset:
        for d in dataset:
            if d == "hnscc":
                data = hnscc
            if d == "hn_one":
                data = hn_one
            if d == "head_neck":
                data = head_neck
            if d == "opc":
                data = opc
            result = result.append(data)
        # print(result)
        if (result.empty == False):
            fig = px.sunburst(result, path=['Gender', 'AJCC', 'TumourLocation'], color='AJCC')
            fig.update_layout(title_text='Gender & Stage-wise Tumour Location', title_x=0.5)
            return fig
        else:
            fig = px.sunburst(None)
            return fig
    else:
        fig = px.sunburst(None)
        return fig

@app.callback(
    Output("scatter", "figure"),
    [Input("dataset", "value"),
     Input("columns", "value")])
def update_scatter(dataset, columns):
    result = pd.DataFrame()
    if dataset:
        for d in dataset:
            if d == "hnscc":
                data = result_age_hnscc
            if d == "hn_one":
                data = result_age_hn_one
            if d == "head_neck":
                data = result_age_hn
            if d == "opc":
                data = result_age_opc
            result = result.append(data)
        result['Age_Range'] = pd.cut(result['agevalue'], [0, 40, 50, 60, 70, 80, 90],
                                     labels=['0-40', '40-50', '50-60', '60-70', '70-80', '80-90'])
        x = result.groupby(['Age_Range']).count()
        if (x.empty == False):
            fig = px.scatter(x, color_discrete_sequence=px.colors.qualitative.Antique, size='value', color='value')
            fig.update_layout(title_text='Cases per Age_range', title_x=0.5)
            fig.update_traces(hovertemplate='Age_range: %{x} <br>Count: %{y}')
            return fig
        else:
            fig = px.scatter(None)
            return fig
    else:
        fig = px.scatter(None)
        return fig

#@app.callback(
#    Output("box", "figure"),
#    [Input("dataset", "value"),
#     Input("columns", "value")])
#def update_box(dataset, columns):
#    result = pd.DataFrame()
#    x = 0
#    if dataset:
#        for d in dataset:
#            result_data = queryresult(d, queryAgeSurv)
#            data = pd.read_csv(StringIO(result_data))
#            result = result.append(data)
#        result['Age_Range'] = pd.cut(result['agevalue'], [0, 40, 50, 60, 70, 80, 90],
#                                     labels=['0-40', '40-50', '50-60', '60-70', '70-80', '80-90'])
#        result.dropna(subset=["survivaldays"], inplace=True)  # drops NaN
#        result = result.sort_values("Age_Range").reset_index(drop=True)
#        result["survival"].replace(codedict, inplace=True)
        # print(result)
#        if (result.empty == False):
#            fig = px.box(result, x='Age_Range', y='survivaldays', notched=False, color='survival')
#            fig.update_layout(title_text='Survival days by age', title_x=0.5)
#            return fig
#        else:
#            fig = px.box(None)
#            return fig
#    else:
#        fig = px.box(None)
#        return fig

@app.callback(
    Output("pie-chart", "figure"),
    [Input("dataset", "value"),
     Input("columns", "value")])
def generate_chart(dataset, columns):
    result = pd.DataFrame()
    result_data = ''
    if dataset:
        for d in dataset:
            if d == "hnscc":
                data = result_hnscc
            if d == "hn_one":
                data = result_hn_one
            if d == "head_neck":
                data = result_hn
            if d == "opc":
                data = result_opc
            result = result.append(data)
        # print(result)
        if (result.empty == False):
            fig = px.pie(result, names=result[columns], color_discrete_sequence=px.colors.sequential.RdBu)
            return fig
        else:
            fig = px.pie(None)
            return fig
    else:
        fig = px.pie(None)
        return fig

@app.callback(
    Output("loading-output-2", "children"),
    Input("dataset", "value"))
def input_triggers_nested(value):
    time.sleep(2)

if __name__ == '__main__':
    app.run_server(debug=True, host ='0.0.0.0')
