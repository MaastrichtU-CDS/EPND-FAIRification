from flaskr.services.triplestore import AbstractTripleStore

class FipService:
    def __init__(self, triplestore: AbstractTripleStore):
        self.__triplestore = triplestore
    
    def load_fip(self, uri, triples):
        query = f"INSERT {{ GRAPH <{uri}> {{ {triples} }} }} WHERE {{ }}"
        self.__triplestore.update_sparql(query)