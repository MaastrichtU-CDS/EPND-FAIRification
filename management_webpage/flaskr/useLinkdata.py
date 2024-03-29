import pandas as pd
import sparql_dataframe as sd
from SPARQLWrapper import SPARQLWrapper
from flask import current_app

#Add a new link
def createLink(datasetId, value1, value2):
    endpointUrl = current_app.config.get("rdf_endpoint")
    endpoint = SPARQLWrapper(endpointUrl + '/statements')
    graph = "http://mapping.local/" + str(datasetId) + "/"
    q = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
insert {{
    GRAPH <{}> {{
        <{}>
            owl:equivalentClass <{}>
        }}
    }} where {{ }}
    """.format(graph, value1, value2)
    endpoint.setQuery(q)
    endpoint.method = 'POST'
    endpoint.query()

def createCellLink(target, superClass, value, datasetId):
    endpointUrl = current_app.config.get("rdf_endpoint")
    endpoint = SPARQLWrapper(endpointUrl + '/statements')
    q='''
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    INSERT {
        GRAPH <http://data.local/mapping/%s> {
            dbo:cell_of rdf:type owl:ObjectProperty;
                 owl:inverseOf dbo:has_cell.
            <%s> rdf:type owl:Class ;
                owl:equivalentClass [ 
                    owl:intersectionOf 
                        ( [ 
                            rdf:type owl:Restriction ;
                            owl:onProperty dbo:cell_of ;
                            owl:someValuesFrom <%s>;
                        ]
                        [ 
                            rdf:type owl:Restriction ;
                            owl:onProperty dbo:has_value ;
                            owl:hasValue "%s"^^xsd:string;
                        ]
                        ) ;
                        rdf:type owl:Class;
                    ].
            } } WHERE { }
    '''%(datasetId, target, superClass, value)
    endpoint.setQuery(q)
    endpoint.method = 'POST'
    endpoint.query()

# Delete cell mappings
def deleteCellLinks(target, oldValue, cdmValue, cellValue, datasetId):
    endpointUrl = current_app.config.get("rdf_endpoint")
    endpoint = SPARQLWrapper(endpointUrl + '/statements')
    q = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>    
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    WITH <http://data.local/mapping/%s>
    DELETE{
        <%s> owl:equivalentClass ?o.
    }
    INSERT{
        <%s> owl:equivalentClass ?o.
    }
    WHERE{
        dbo:cell_of rdf:type owl:ObjectProperty;
                    owl:inverseOf dbo:has_cell.
        <%s> rdf:type owl:Class ;
             owl:equivalentClass ?o.
        ?o owl:intersectionOf([
            rdf:type owl:Restriction ;
            owl:onProperty dbo:cell_of ;
            owl:someValuesFrom <%s>;
        ]
        [
            rdf:type owl:Restriction ;
            owl:onProperty dbo:has_value ;
            owl:hasValue "%s"^^xsd:string;
        ]
        );
        rdf:type owl:Class;
    }
    """%(datasetId, oldValue, target, oldValue, cdmValue, cellValue)
    print(q)
    endpoint.setQuery(q)
    endpoint.method = 'POST'
    endpoint.query()
    
    print('Deletion complete')

#Delete links for remapping from an actual value to UNKNOWN
def deleteCellLinksNoInsert(oldValue, cdmValue, cellValue, datasetId):
    endpointUrl = current_app.config.get("rdf_endpoint")
    endpoint = SPARQLWrapper(endpointUrl + '/statements')
    q = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>    
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    WITH <http://data.local/mapping/%s>
    DELETE{
        ?targetClass owl:equivalentClass ?o;
                     rdf:type owl:Class.
        ?o rdf:type owl:Class;
           owl:intersectionOf ?o1.
        ?o1 rdf:first ?o2;
            rdf:rest ?o3.
        ?o2 owl:onProperty dbo:cell_of;
            owl:someValuesFrom ?cdm;
            rdf:type owl:Restriction.
        ?o3 rdf:first ?o4;
            rdf:rest rdf:nil.
        ?o4 rdf:type owl:Restriction;
            owl:hasValue ?value;
            owl:onProperty dbo:has_value.
    }
    WHERE{
        BIND(<%s> as ?targetClass)
        BIND(<%s> as ?cdm)
        ?targetClass owl:equivalentClass ?o;
                 rdf:type owl:Class.
        ?o rdf:type owl:Class;
           owl:intersectionOf ?o1.
        ?o1 rdf:first ?o2;
            rdf:rest ?o3.
        ?o2 owl:onProperty dbo:cell_of;
            owl:someValuesFrom ?cdm;
            rdf:type owl:Restriction.
        ?o3 rdf:first ?o4;
            rdf:rest rdf:nil.
        ?o4 rdf:type owl:Restriction;
            owl:hasValue ?value;
            owl:onProperty dbo:has_value.
        VALUES (?value){("%s")}
    }
    """%(datasetId, oldValue, cdmValue, cellValue)
    print(q)
    endpoint.setQuery(q)
    endpoint.method = 'POST'
    endpoint.query()
    
    print('Deletion complete')

#Delete a existing link
def deleteLink(datasetId, cdmUri, datasetUri):
    print('start deletion')
    endpointUrl = current_app.config.get("rdf_endpoint")
    endpoint = SPARQLWrapper(endpointUrl + '/statements')
    q = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    delete {{
        GRAPH <http://mapping.local/{}/> {{
            <{}> owl:equivalentClass <{}>
        }}
    }} where {{ }} 

    """.format(datasetId, datasetUri, cdmUri)
    print(q)
    endpoint.setQuery(q)
    endpoint.method = 'POST'
    endpoint.query()
    print('end deletion')

#Retrieves all mapped values
def retrieveMappings(datasetId):
    endpoint = current_app.config.get("rdf_endpoint")
    q = """
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix sh: <http://www.w3.org/ns/shacl#>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    prefix sio: <http://semanticscience.org/resource/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>

    SELECT ?cdmUri ?cdmUriLabel ?columnName ?columnUri
    WHERE {
                GRAPH <http://mapping.local/%s/> {
                ?columnUri owl:equivalentClass ?cdmUri
            }
                ?columnUri rdfs:subClassOf dbo:ColumnCell;
                    dbo:column ?columnName;
                    dbo:table ?tableUri.
                ?tableUri dbo:table ?tableName.
        
        ?nodeShape rdf:type sh:NodeShape;
            sh:targetClass ?cdmUri.

        OPTIONAL {
            ?cdmUri rdfs:label ?cdmUriLabel.
        }

        
        ## Units are always their own instance (measurement -> unit -> literal), therefore filtering the unit instances.
        FILTER (!(STRSTARTS(str(?cdmUri), "http://purl.obolibrary.org/obo/UO_"))).
        FILTER (?cdmUri != sio:SIO_001112).
    }
    """%(datasetId)
    df = sd.get(endpoint, q)
    return df

#Retrieves the dataset columns both mapped and not mapped
def retrieveDatasetMapped(datasetId):
    print(current_app.config)
    endpoint = current_app.config.get("rdf_endpoint")
    graph = "http://mapping.local/" + str(datasetId) + "/"
    q = """    
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    prefix sh: <http://www.w3.org/ns/shacl#>
    prefix xsd: <http://www.w3.org/2001/XMLSchema#>
    prefix sio: <http://semanticscience.org/resource/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
    SELECT ?cdmUri ?cdmUriLabel ?columnName ?columnUri
    WHERE {
        ?columnUri rdfs:subClassOf dbo:ColumnCell;
                   dbo:column ?columnName;
                   dbo:table ?tableUri.
        ?tableUri dbo:table ?tableName.
        optional{
            GRAPH <%s> {
                ?columnUri owl:equivalentClass ?cdmUri
            }
            ?columnUri rdfs:subClassOf dbo:ColumnCell;
                       dbo:column ?columnName;
                       dbo:table ?tableUri.
            ?tableUri dbo:table ?tableName.
            ?nodeShape rdf:type sh:NodeShape;
                       sh:targetClass ?cdmUri.
            OPTIONAL {
                ?cdmUri rdfs:label ?cdmUriLabel.
            }
            ## Units are always their own instance (measurement -> unit -> literal), therefore filtering the unit instances.
            FILTER (!(STRSTARTS(str(?cdmUri), "http://purl.obolibrary.org/obo/UO_"))).
            FILTER (?cdmUri != sio:SIO_001112).
        }
    }"""%(graph)
    print(q)
    df = sd.get(endpoint, q)
    return df
