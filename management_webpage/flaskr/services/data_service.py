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