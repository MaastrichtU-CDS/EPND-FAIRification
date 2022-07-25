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