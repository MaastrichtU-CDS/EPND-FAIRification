from flaskr.services.triplestore import AbstractTripleStore
import logging

class CedarEndpoint:
    def __init__(self, triplestore: AbstractTripleStore):
        """
        The CedarEndpoint class manages communication to the SPARQL endpoint.
        triplestore: implementation of AbstractTripleStore
        """
        self.__triplestore = triplestore
    
    def get_template_location(self):
        """
        Retrieve the cedar template location (JSON file location)
        """
        query = """
            prefix sio: <http://semanticscience.org/resource/>
            
            SELECT DISTINCT ?cedar_template
            WHERE {
                ?template_obj_uri rdf:type <https://schema.metadatacenter.org/core/Template>;
                    sio:SIO_000628 ?cedar_template;
            }
        """
        return self.__triplestore.select_sparql(query)[0]["cedar_template"]["value"]

    def list_instances(self):
        """
        Retrieve all instances stored in the SPARQL endpoint
        """
        
        query = """
        prefix pav: <http://purl.org/pav/>

        select distinct ?instance ?time
        where { 
            ?instance pav:createdOn ?time.
        }
        """

        return self.__triplestore.select_sparql(query)
    
    def describe_instance(self, instance_uri):
        """
        Retrieve the direct properties of the given instance
        """
        query = """
        SELECT ?predicate ?object
        WHERE {
            <%s> ?predicate ?object.
        }
        """ % instance_uri
        return self.__triplestore.select_sparql(query)
    
    def get_instance_links(self, instance_uri):
        """
        Retrieve the references of this instance
        """
        query = """
        SELECT ?predicate ?object
        WHERE {
            ?subject ?predicate <%s>.
        }
        """ % instance_uri
        return self.__triplestore.select_sparql(query)

    def drop_instance(self, identifier):
        """
        Delete the form instance
        """
        query = "DROP GRAPH <%s>" % identifier
        logging.debug(query)

        results = self.__triplestore.update_sparql(query)
        logging.debug(results.response.read())

    def store_instance(self, rdf_string, graph_uri=None):
        """
        Store data to a SPARQL endpoint.
        rdf_string: containing the triples (format=nt) to store
        graph_uri: optional, to set the named graph
        """
        queryData = "INSERT DATA { %s }" % rdf_string
        if graph_uri is not None:
            queryData = "INSERT DATA { GRAPH <%s> { %s } }" % (graph_uri, rdf_string)

        logging.debug(queryData)

        results = self.__triplestore.update_sparql(queryData)
        logging.debug(results.response.read())