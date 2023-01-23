from flaskr.services.triplestore import AbstractTripleStore
import logging

class CedarEndpoint:
    def __init__(self, triplestore: AbstractTripleStore, metadata_title_predicate=None):
        """
        The CedarEndpoint class manages communication to the SPARQL endpoint.
        triplestore: implementation of AbstractTripleStore
        """
        self.__triplestore = triplestore
        # TODO: make this variable configurable, needs to be put into the FIP (e.g. "http://purl.org/dc/terms/title")
        self.__predicate_name_metadata_instance = metadata_title_predicate
    
    def get_template_location(self):
        """
        Retrieve the cedar template location (JSON file location)
        """
        query = """
            prefix sio: <http://semanticscience.org/resource/>
            prefix schema: <https://schema.org/>
            
            SELECT DISTINCT ?cedar_template
            WHERE {
                ?template_obj_uri rdf:type <https://schema.metadatacenter.org/core/Template>;
                    sio:SIO_000628 [
                        schema:distribution [
                            schema:encodingFormat "application/ld+json";
                            schema:contentUrl ?cedar_template;
                        ];
                    ].
            }
        """
        return self.__triplestore.select_sparql(query)[0]["cedar_template"]["value"]
    
    def get_instance_name_for_uri(self, instanceUri):
        """
        Retrieve the title for the instance used
        """

        if self.__predicate_name_metadata_instance is None:
            return ""

        query = """
        SELECT ?name
        WHERE {
            <%s> <%s> ?name.
        }
        """ % (instanceUri, self.__predicate_name_metadata_instance)

        queryResult = self.__triplestore.select_sparql(query)

        if len(queryResult == 0):
            return ""
        else :
            return self.__triplestore.select_sparql(query)[0]["name"]["value"]

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

        if self.__predicate_name_metadata_instance is not None:
            query = f"""
            prefix pav: <http://purl.org/pav/>

            select distinct ?instance ?time ?label
            where {{ 
                ?instance pav:createdOn ?time;
                    <{self.__predicate_name_metadata_instance}> ?label.
            }}
            """

        return self.__triplestore.select_sparql(query)
    
    def describe_instance(self, instance_uri):
        """
        Retrieve the direct properties of the given instance
        """
        query = """
        prefix dcat: <http://www.w3.org/ns/dcat#>
        SELECT ?predicate ?object
        WHERE {
            <%s> ?predicate ?object.
            FILTER (?predicate NOT IN (dcat:distribution))
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
        logging.debug(results)

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
        logging.debug(results)