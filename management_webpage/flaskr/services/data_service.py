from flaskr.services.triplestore import AbstractTripleStore
import logging

class DataEndpoint:
    def __init__(self, triplestore: AbstractTripleStore):
        """
        The DataEndpoint class manages communication to the SPARQL endpoint.
        triplestore: implementation of AbstractTripleStore
        """
        self.__triplestore = triplestore
    
    def store_cedar_task_link(self, cedarUri, taskUri):
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
                        dcat:mediaType "rdf";
                    ].
                }
            } WHERE { }
        """ % (cedarUri, taskUri)
        logging.debug(query)

        results = self.__triplestore.update_sparql(query)
        logging.debug(results)