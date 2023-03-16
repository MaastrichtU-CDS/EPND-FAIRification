import sparql_dataframe as sd
from flask import current_app

class NanopubService:
    def __init__(self, uri):
        self.uri = uri

    def parse_shacl_uri(self):
        # Query the sparql endpoint to obtain the results
        # https://virtuoso.nps.petapico.org/sparql
        endpoint = current_app.config.get("nanopub_endpoint")
        q = """
        PREFIX np: <http://www.nanopub.org/nschema#>
        PREFIX fip: <https://w3id.org/fair/fip/terms/>
        SELECT distinct ?shacl WHERE {
            ?np a np:Nanopublication;
                np:hasAssertion ?assert;
                np:hasProvenance ?prov;
                np:hasPublicationInfo ?pInfo ;
                <http://purl.org/nanopub/x/includesElement> ?element.
            ?element np:hasAssertion ?sub_element.
            GRAPH ?sub_element {
                ?a fip:refers-to-question fip:FIP-Question-I2-D;
                    fip:declares-planned-use-of ?shacl_link.
            }
            bind(URI(strbefore(str(?shacl_link), "#")) as ?shacl_link_temp)
            ?shacl_link_temp np:hasAssertion ?shacl_assertion.
            GRAPH ?shacl_assertion{
                ?b <http://usefulinc.com/ns/doap#implements> ?shacl;
                    a <fip:Available-FAIR-Enabling-Resource> ,\
                    fip:FAIR-Enabling-Resource , \
                    fip:Structured-vocabulary .
            }
            FILTER(str(?np) = "%s")
        }
        """%self.uri
        df = sd.get(endpoint, q)
        shacl_uri = df['shacl'][0]
        q = '''
        PREFIX np: <http://www.nanopub.org/nschema#>
        PREFIX fip: <https://w3id.org/fair/fip/terms/>

        SELECT distinct ?cedar WHERE {
            ?np a np:Nanopublication;
                np:hasAssertion ?assert;
                np:hasProvenance ?prov;
                np:hasPublicationInfo ?pInfo ;
                <http://purl.org/nanopub/x/includesElement> ?element.
            ?element np:hasAssertion ?sub_element.
            GRAPH ?sub_element {
                ?a fip:refers-to-question fip:FIP-Question-I3-MD;
                    fip:declares-planned-use-of ?cedar_link.
            }
            bind(URI(strbefore(str(?cedar_link), "#")) as ?cedar_link_temp)
            ?cedar_link_temp np:hasAssertion ?cedar_assertion.
            GRAPH ?cedar_assertion{
                ?b <http://usefulinc.com/ns/doap#implements> ?cedar.
            }
            FILTER(str(?np) = "%s")
        }
        '''%self.uri
        df = sd.get(endpoint, q)
        cedar_uri = df['cedar'][0]
        if shacl_uri and cedar_uri:
            fip_uri = self.create_fip_uri(shacl_uri, cedar_uri)
            return fip_uri

    def create_fip_uri(self, shacl_uri, cedar_uri):
        base_fip = """
        @prefix local: <#> .
        @prefix fip: <https://w3id.org/fair/fip/terms/> .
        @prefix dash: <http://datashapes.org/dash#> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix sh: <http://www.w3.org/ns/shacl#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        @prefix sio: <http://semanticscience.org/resource/>.
        @prefix snomed: <http://purl.bioontology.org/ontology/SNOMEDCT/>.
        @prefix UO: <http://purl.obolibrary.org/obo/>.
        @prefix sty: <http://purl.bioontology.org/ontology/STY/>.
        @prefix loinc: <http://purl.bioontology.org/ontology/LNC/>.
        @prefix sh: <http://www.w3.org/ns/shacl#>.
        @prefix schema: <https://schema.org/>.

        local:myFip rdf:type fip:FIP-Declaration;
                    rdfs:label "EPND use case 1 ATN";
                    fip:declares-current-use-of [
                        rdf:type <https://schema.metadatacenter.org/core/Template>;
                        sio:SIO_000628 <https://repo.metadatacenter.org/templates/cda2f30a-6b9c-4210-a87d-be78a416fdd4>;
                    ];
                    fip:declares-current-use-of [
                        sh:shapesGraph <shacl_uri>;
                     ].

        <https://repo.metadatacenter.org/templates/cda2f30a-6b9c-4210-a87d-be78a416fdd4> schema:distribution [
                schema:encodingFormat "application/ld+json";
                schema:contentUrl <cedar_uri>;
        ]."""
        base_fip = base_fip.replace('shacl_uri', shacl_uri)
        return base_fip.replace('cedar_uri', cedar_uri)

