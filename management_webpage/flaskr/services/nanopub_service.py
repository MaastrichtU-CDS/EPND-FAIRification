from nanopub import Nanopub
from rdflib import URIRef 
import re

class NanopubService:
    def __init__(self, uri):
        self.uri = uri

    def parse_shacl_uri(self):
        np = Nanopub(self.uri)
        for s, p, o in np.assertion:
            for s1, p1, o1 in Nanopub(o).assertion:
                if o1 ==\
                URIRef("https://w3id.org/fair/fip/terms/FIP-Question-I2-D")\
                and\
                p1 ==\
                URIRef("https://w3id.org/fair/fip/terms/refers-to-question"):
                    for s2, p2, o2 in Nanopub(o).assertion:
                        if p2 ==\
                        URIRef("https://w3id.org/fair/fip/terms/declares-planned-use-of"):
                            for s3, p3, o3 in Nanopub(re.split('#',
                                                               o2)[0]).assertion:
                                if p3 ==\
                                URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso"):
                                    #return o1
                                    return \
                                "https://raw.githubusercontent.com/MaastrichtU-CDS/EPND-FAIRification/main/fip/fip.ttl"
