from nanopub import Nanopub
from rdflib import URIRef 
import re

class NanopubService:
    def __init__(self, uri):
        self.uri = uri

    def fetch_np(self, np): 
        try:
            np_parsed = Nanopub(np)
        except ConnectionError as e:
            raise Exception("Connection refused by server,\
                    please try after a while")
        return np_parsed

    def parse_shacl_uri(self):
        np = self.fetch_np(self.uri)
        for s, p, o in np.assertion:
            for s1, p1, o1 in self.fetch_np(o).assertion:
                if o1 ==\
                URIRef("https://w3id.org/fair/fip/terms/FIP-Question-I2-D")\
                and\
                p1 ==\
                URIRef("https://w3id.org/fair/fip/terms/refers-to-question"):
                    for s2, p2, o2 in self.fetch_np(o).assertion:
                        if p2 ==\
                        URIRef("https://w3id.org/fair/fip/terms/declares-planned-use-of"):
                            o2_parsed = re.split('#', o2)[0]
                            for s3, p3, o3 in self.fetch_np(o2_parsed).assertion:
                                if p3 ==\
                                URIRef("http://usefulinc.com/ns/doap#implements"):
                                    shacl_uri = o3
                                    break
                if o1 ==\
                URIRef("https://w3id.org/fair/fip/terms/FIP-Question-I3-MD")\
                and p1 ==\
                URIRef("https://w3id.org/fair/fip/terms/refers-to-question"):
                    for s2, p2, o2 in self.fetch_np(o).assertion:
                        if p2 ==\
                        URIRef("https://w3id.org/fair/fip/terms/declares-planned-use-of"):
                            o2_parsed = re.split('#', o2)[0]
                            for s3, p3, o3 in\
                            self.fetch_np(o2_parsed).assertion:
                                if p3 ==\
                                        URIRef("http://usefulinc.com/ns/doap#implements"):
                                            cedar_uri = o3
                                            break
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

