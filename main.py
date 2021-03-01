import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import pandas as pd
from io import StringIO

def queryresult(repo):
    endpoint = "http://docker-graphdb-root-johan-graphdb.app.dsri.unimaas.nl/repositories/"+repo
    query = """
    PREFIX db: <http://localhost/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?genderCode ?tstageCode ?nstageCode ?survivalCode

    WHERE {
    
    ?tablerow roo:P100018 ?gender.
    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100244 ?tstage.
    ?neoplasm roo:P100242 ?nstage.
    #?neoplasm roo:P100241 ?mstage.
    ?tablerow roo:P100254 ?survival.

    BIND(strafter(str(?tablerow), "http://172.20.10.14/rdf/data/") AS ?patient)

    OPTIONAL
    {
        ?gender a ?g.
        ?tstage a ?t.
        ?nstage a ?n.
        #?mstage a ?m.
        ?survival a ?s.
  
   		FILTER regex(str(?g), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197"))
        FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732"))
        FILTER regex(str(?n), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48705|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48706|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48786|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48714"))
        #FILTER regex(str(?m), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48699|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48700"))
        FILTER regex(str(?s), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C28554|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C37987"))
  		BIND(strafter(str(?g), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?genderCode)
        BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?tstageCode)
        BIND(strafter(str(?n), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?nstageCode)
        #BIND(strafter(str(?m), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?mstageCode)
        BIND(strafter(str(?s), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?survivalCode)

    }
}
            """

    annotationResponse = requests.post(endpoint,
                                       data="query=" + query,
                                       headers={
                                           "Content-Type": "application/x-www-form-urlencoded",
                                           # "Accept": "application/json"
                                       })
    output = annotationResponse.text
    # print(annotationResponse.text)
    #f = open("csv_output.csv", 'w', newline='')
    #f.write(output)
    #f.close()
    return output

#data = pd.read_csv("csv_output.csv")

app = dash.Dash(__name__)

app.layout = html.Div(
     [
    html.P("Columns:"),
    dcc.Dropdown(
        id='columns',
        value='genderCode',
        options=[{'label': 'Gender', 'value': 'genderCode'},
                 {'label': 'Tstage', 'value': 'tstageCode'},
                 {'label': 'Nstage', 'value': 'nstageCode'},
                 {'label': 'Survival Status', 'value': 'survivalCode'}],
        clearable=False ),
    html.P("Dataset:"),
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
    dcc.Graph(id="pie-chart")
])


@app.callback(
    Output("pie-chart", "figure"),
    [Input("dataset", "value"),
     Input("columns", "value")])
def generate_chart(dataset, columns):
    result = pd.DataFrame()
    for d in dataset:
        result_data = queryresult(d)
        data = pd.read_csv(StringIO(result_data))
        result = result.append(data)
    fig = px.pie(result, names=result[columns], color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

app.run_server(debug=True)
