from flaskr.services.triplestore import AbstractTripleStore
import rdflib

class FipService:
    def __init__(self, triplestore: AbstractTripleStore):
        self.__triplestore = triplestore
    
    def load_fip(self, uri, triples):
        return self.__triplestore.upload_turtle(triples, uri)
    
    def get_fip(self):
        return self.__triplestore.select_sparql("""
            prefix fip: <https://w3id.org/fair/fip/terms/>
            prefix sio: <http://semanticscience.org/resource/>
            prefix sh: <http://www.w3.org/ns/shacl#>
            
            SELECT DISTINCT ?fip ?fip_label ?cedar_template ?shacl_location
            WHERE {
                ?fip rdf:type fip:FIP-Declaration;
                    fip:declares-current-use-of [
                        rdf:type <https://schema.metadatacenter.org/core/Template>;
                        sio:SIO_000628 ?cedar_template;
                    ];
                    fip:declares-current-use-of [
                        sh:shapesGraph ?shacl_location;
                    ].
                OPTIONAL { ?fip rdfs:label ?fip_label; }
            }""")
    
    def cache_shacl(self):
        fips = self.get_fip()
        for fip in fips:
            shacl_location = fip["shacl_location"]["value"]
            try:
                g = rdflib.Graph()
                g.parse(shacl_location, format="turtle")
            except Exception as e:
                print("Could not load the SHACL file at %s - Is the URL correct?" % shacl_location)
                pass
            
            triples = g.serialize(format="turtle")
            self.__triplestore.upload_turtle(triples, shacl_location)