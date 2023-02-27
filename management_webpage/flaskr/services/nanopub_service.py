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
                                    return o3 
