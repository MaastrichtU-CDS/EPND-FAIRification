import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import pandas as pd
import csv

# This dataframe has 244 lines, but 4 distinct values for `day`
#df = px.data.tips()

def queryresult():
    endpoint = "http://docker-graphdb-root-johan-graphdb.app.dsri.unimaas.nl/repositories/Varsha_tcia"

    query = """
    PREFIX db: <http://localhost/rdf/ontology/>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX roo: <http://www.cancerdata.org/roo/>
    PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?patient ?IDvalue ?agevalue ?gendervalue ?genderCode ?tstageCode

    WHERE {
   
    ?tablerow roo:P100061 ?patientID.
    ?tablerow roo:hasage ?age. 
    ?tablerow roo:P100018 ?gender.
    ?tablerow roo:P100029 ?neoplasm.
    ?neoplasm roo:P100244 ?tstage.
  
    ?patientID roo:P100042 ?IDvalue. 
    ?age roo:P100042 ?agevalue.
    ?gender roo:P100042 ?gendervalue.
    ?tstage roo:P100042 ?tstagevalue.
    
    BIND(strafter(str(?tablerow), "http://172.20.10.14/rdf/data/") AS ?patient)
 
    OPTIONAL
    {
        ?gender a ?s.
        ?tstage a ?t.
  
  		#BIND(strafter(str(?tablerow), "http://172.20.10.14/rdf/data/") AS ?patient)
   		FILTER regex(str(?s), 		("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C16576|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C20197"))
        FILTER regex(str(?t), ("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48719|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48720|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48724|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48728|http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#C48732"))
  		BIND(strafter(str(?s), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?genderCode)
        BIND(strafter(str(?t), "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#") AS ?tstageCode)
    
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

    f = open("csv_output.csv", 'w', newline='')
    f.write(output)
    f.close()

queryresult()

data = pd.read_csv("csv_output.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Columns:"),
    dcc.Dropdown(
        id='columns',
        value='genderCode',
        options=[{'label': 'Gender', 'value': 'genderCode'},
                 {'label': 'Tstage', 'value': 'tstageCode'}],
        clearable=False
    ),
    html.P("Dataset:"),
    dcc.Checklist(
        id = 'dataset',
        options=[
        {'label': 'Maastricht', 'value': 'triplifier_test_HN_Maastricht'},
        {'label': 'Montréal', 'value': 'triplifier_test_HN_Montreal'},
        {'label': 'Houston', 'value': 'triplifier_test_HN_Houston'},
        {'label': 'Toronto', 'value': 'triplifier_test_HN_Toronto'}
    ],
    value=['triplifier_test_HN_Maastricht'],
    labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="pie-chart"),
    dcc.Graph(id='Boxplot')
])

@app.callback(
    Output("pie-chart", "figure"), 
    [Input("dataset", "value"),
        Input("columns", "value")])
def generate_chart(dataset, columns):
    result = pd.DataFrame()
    for d in dataset:
        var = data[data['patient'].str.contains(d)]
        result = result.append(var)
    #print(result)
    fig = px.pie(data, names=result[columns], color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

app.run_server(debug=True)
