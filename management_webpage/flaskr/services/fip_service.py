from flaskr.services.triplestore import AbstractTripleStore

class FipService:
    def __init__(self, triplestore: AbstractTripleStore):
        self.__triplestore = triplestore
    
    def load_fip(self, uri, triples):
        query = f"INSERT {{ GRAPH <{uri}> {{ {triples} }} }} WHERE {{ }}"
        self.__triplestore.update_sparql(query)
    
    def get_fip(self):
        return self.__triplestore.select_sparql("""
            prefix fip: <https://w3id.org/fair/fip/terms/>
            prefix sio: <http://semanticscience.org/resource/>
            
            SELECT DISTINCT ?fip ?fip_label ?cedar_template
            WHERE {
                ?fip rdf:type fip:FIP-Declaration;
                    fip:declares-current-use-of [
                        rdf:type <https://schema.metadatacenter.org/core/Template>;
                        sio:SIO_000628 ?cedar_template;
                    ].
                OPTIONAL { ?fip rdfs:label ?fip_label; }
            }""")