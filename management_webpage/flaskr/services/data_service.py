from flaskr.services.triplestore import AbstractTripleStore
import logging

class DataEndpoint:
    def __init__(self, triplestore: AbstractTripleStore):
        """
        The DataEndpoint class manages communication to the SPARQL endpoint.
        triplestore: implementation of AbstractTripleStore
        """
        self.__triplestore = triplestore
    
    def store_cedar_task_link(self, cedarUri, dataUri, ontologyUri, taskId):
        """
        Store the link between a Cedar instance URI, and the TaskURI used as context in the RDF store.
        """
        query = """
            prefix dcat: <http://www.w3.org/ns/dcat#>
            INSERT {
                GRAPH <http://distributions.local/> {
                    <%s> dcat:distribution [
                        dcat:accessService "SPARQL";
                        dcat:accessUrl <%s>;
                        dcat:conformsTo <%s>;
                        dcat:mediaType "rdf";
                        dcat:identifier "%s";
                    ].
                }
            } WHERE { }
        """ % (cedarUri, dataUri, ontologyUri, taskId)
        logging.debug(query)

        results = self.__triplestore.update_sparql(query)
        logging.debug(results)
    
    def get_distributions_for_metadata(self, cedarUri):
        """
        Retrieve datasets for a given cedar template
        """

        query = """
            prefix dcat: <http://www.w3.org/ns/dcat#>
            SELECT ?distributionUri ?ontologyUri ?identifier
            WHERE {
                GRAPH <http://distributions.local/> {
                    <%s> dcat:distribution [
                        dcat:accessService "SPARQL";
                        dcat:accessUrl ?distributionUri;
                        dcat:conformsTo ?ontologyUri;
                        dcat:mediaType "rdf";
                        dcat:identifier ?identifier;
                    ].
                }
            }
        """ % cedarUri

        return self.__triplestore.select_sparql(query)
    
    def get_tables_for_distribution(self, ontologyUri):
        """
        Retrieve datasets for a given cedar template
        """

        query = """
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?table
            FROM <%s>
            WHERE {
                ?subject dbo:table ?table;
                        rdfs:subClassOf dbo:TableRow.
            }
        """ % ontologyUri

        print(query)

        return self.__triplestore.select_sparql(query)
    
    def get_fip_and_shacl_for_cedar_instance(self, instanceUrl):
        return self.__triplestore.select_sparql("""
            PREFIX sh: <http://www.w3.org/ns/shacl#>
            PREFIX schema: <http://schema.org/>
            PREFIX sio: <http://semanticscience.org/resource/>
            PREFIX local: <https://raw.githubusercontent.com/MaastrichtU-CDS/EPND-FAIRification/main/fip/fip.ttl#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX fip: <https://w3id.org/fair/fip/terms/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            select distinct ?fip ?shapesGraph where {
                <%s> schema:isBasedOn ?cedarTemplate.
                
                ?fip rdf:type fip:FIP-Declaration;
                    fip:declares-current-use-of [
                        rdf:type <https://schema.metadatacenter.org/core/Template>;
                        sio:SIO_000628 ?cedarTemplate;
                    ];
                    fip:declares-current-use-of [
                        sh:shapesGraph ?shapesGraph;
                    ].
            }

            """ % instanceUrl)
    
    def get_mapped_shapes_from_shacl(self, shaclUri):
        # The last line in the query below limits to only mapped columns
        results = self.__triplestore.select_sparql("""
            PREFIX sh: <http://www.w3.org/ns/shacl#>
            PREFIX sio: <http://semanticscience.org/resource/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            prefix epnd: <https://raw.githubusercontent.com/MaastrichtU-CDS/EPND-FAIRification/main/management_webpage/shapeTest/shacl.ttl#>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>

            select ?shape ?targetClass ?targetClassLabel ?variableType ?variableTypeLabel ?columnClass ?columnName
            where {
                {
                    ?shape rdf:type sh:NodeShape.
                    FILTER(isUri(?shape) && STRSTARTS(STR(?shape), STR(epnd:)))
                } MINUS {
                    ?shape sh:property [
                        sh:path sio:SIO_000300;
                    ].
                }
                
                ?shape sh:targetClass ?targetClass.
                ?targetClass rdfs:label ?targetClassLabel.
                
                OPTIONAL {
                    ?shape rdf:type ?variableType.
                    FILTER( ?variableType not in (owl:Thing, sh:NodeShape ) ).
                    OPTIONAL { ?variableType rdfs:label ?variableTypeLabel }.
                }

                ?targetClass owl:equivalentClass ?columnClass.
                ?columnClass dbo:column ?columnName.
            }"""
        )

        return self.__triplestore.get_values_from_results(results)
    
    def get_data_for_column_class(self, listWithColumnClass):
        query = """
            PREFIX sh: <http://www.w3.org/ns/shacl#>
            PREFIX sio: <http://semanticscience.org/resource/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX dbo: <http://um-cds/ontologies/databaseontology/>

            SELECT *
            WHERE {
        """

        for colClassRow in listWithColumnClass:
            query += f"""
                ?row dbo:has_column [
                    rdf:type <{colClassRow['columnClass']}>;
                    dbo:has_cell [
                        dbo:has_value ?{colClassRow['columnName']};
                    ];
                ].
            """
        
        query += " }"

        logging.debug(query)

        results = self.__triplestore.select_sparql(query)
        return self.__triplestore.get_values_from_results(results)
            