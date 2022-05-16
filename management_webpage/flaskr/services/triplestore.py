from abc import ABC, abstractmethod

from SPARQLWrapper import SPARQLWrapper, JSON, GET, POST, POSTDIRECTLY

class AbstractTripleStore(ABC):
    
    @abstractmethod
    def update_sparql(query):
        pass

    @abstractmethod
    def select_sparql(query):
        pass


class GraphDBTripleStore(AbstractTripleStore):

    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(endpoint, updateEndpoint=endpoint + '/statements')

        super().__init__()

    def update_sparql(self, query):
        self.sparql.setQuery(query)
        self.sparql.setMethod(POST)
        self.sparql.setRequestMethod(POSTDIRECTLY)
        results = self.sparql.query()

        self.sparql.resetQuery()

        return results.response.read()

    def select_sparql(self, query):
        self.sparql.setQuery(query)
        self.sparql.setMethod(GET)
        self.sparql.setReturnFormat(JSON)

        results = self.sparql.query().convert()

        self.sparql.resetQuery()

        return results["results"]["bindings"]