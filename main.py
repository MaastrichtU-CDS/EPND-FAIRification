import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import pandas as pd
from io import StringIO
import time

queryT = """
    PREFIX db: <http://localhost/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?patient ?tstageCode

    WHERE {

    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100244 ?tstage.

    BIND(strafter(str(?tablerow), "http://172.20.10.14/rdf/data/") AS ?patient)

    OPTIONAL
    {
        ?tstage a ?t.

        FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732"))

        BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?tstageCode)

    }
    }
            """

queryG = """
    PREFIX db: <http://localhost/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?patient ?genderCode 

    WHERE {

    ?tablerow roo:P100018 ?gender.

    BIND(strafter(str(?tablerow), "http://172.20.10.14/rdf/data/") AS ?patient)


    OPTIONAL
    {
        ?gender a ?g.

        FILTER regex(str(?g), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197"))

        BIND(strafter(str(?g), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?genderCode)

    }
}
"""
queryN = """
    PREFIX db: <http://localhost/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?patient ?nstageCode

    WHERE {

    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100242 ?nstage.

    BIND(strafter(str(?tablerow), "http://172.20.10.14/rdf/data/") AS ?patient)

    OPTIONAL
    {
        ?nstage a ?n.

        FILTER regex(str(?n), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714"))

        BIND(strafter(str(?n), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?nstageCode)

    }
    }
"""
queryM = """
    PREFIX db: <http://localhost/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?patient ?mstageCode

    WHERE {

    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100241 ?mstage.

    BIND(strafter(str(?tablerow), "http://172.20.10.14/rdf/data/") AS ?patient)

    OPTIONAL
    {
        ?mstage a ?m.

        FILTER regex(str(?m), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700"))

        BIND(strafter(str(?m), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?mstageCode)

    }
    }
"""
queryS = """
    PREFIX db: <http://localhost/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?patient ?survivalCode

    WHERE {

    ?tablerow roo:P100254 ?survival.

    BIND(strafter(str(?tablerow), "http://172.20.10.14/rdf/data/") AS ?patient)

    OPTIONAL
    {
        ?survival a ?s.

        FILTER regex(str(?s), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987"))

        BIND(strafter(str(?s), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?survivalCode)
    }
    }
"""


def queryresult(repo, query):
    endpoint = "http://docker-graphdb-root-johan-graphdb.app.dsri.unimaas.nl/repositories/" + repo
    annotationResponse = requests.post(endpoint,
                                       data="query=" + query,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.text
    return output

# data = pd.read_csv("csv_output.csv")

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H3("Columns:"),
        dcc.Dropdown(
            id='columns',
            value='genderCode',
            options=[{'label': 'Gender', 'value': 'genderCode'},
                     {'label': 'Tstage', 'value': 'tstageCode'},
                     {'label': 'Nstage', 'value': 'nstageCode'},
                     {'label': 'Mstage', 'value': 'mstageCode'},
                     {'label': 'Survival Status', 'value': 'survivalCode'}],
            clearable=False),
        html.Div([
            html.H3("Dataset:"),
            dcc.Checklist(
                id='dataset',
                options=[
                    {'label': 'Maastricht', 'value': 'Maastricht'},
                    {'label': 'Montréal', 'value': 'Montreal'},
                    {'label': 'Houston', 'value': 'Houston'},
                    {'label': 'Toronto', 'value': 'Toronto'}
                ],
                value=['Maastricht'],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Loading(
                id="loading-2",
                children=[html.Div([html.Div(id="loading-output-2")])],
                type="default"
            )]),

        dcc.Graph(id="pie-chart")
    ])


@app.callback(
    Output("pie-chart", "figure"),
    [Input("dataset", "value"),
     Input("columns", "value")])
def generate_chart(dataset, columns):
    result = pd.DataFrame()
    for d in dataset:
        if columns == "genderCode":
            result_data = queryresult(d, queryG)
        elif columns == "tstageCode":
            result_data = queryresult(d, queryT)
        elif columns == "nstageCode":
            result_data = queryresult(d, queryN)
        elif columns == "mstageCode":
            result_data = queryresult(d, queryM)
        elif columns == "survivalCode":
            result_data = queryresult(d, queryS)

        data = pd.read_csv(StringIO(result_data))
        result = result.append(data)
        #print(result)

    fig = px.pie(result, names=result[columns], color_discrete_sequence=px.colors.sequential.RdBu)
    return fig


@app.callback(
    Output("loading-output-2", "children"),
    Input("dataset", "value"))
def input_triggers_nested(value):
    time.sleep(2)


app.run_server(debug=True)
