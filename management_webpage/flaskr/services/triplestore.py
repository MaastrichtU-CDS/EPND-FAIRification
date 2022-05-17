from abc import ABC, abstractmethod
from turtle import turtles

from SPARQLWrapper import SPARQLWrapper, JSON, GET, POST, POSTDIRECTLY
import requests

class AbstractTripleStore(ABC):
    
    @abstractmethod
    def update_sparql(query):
        pass

    @abstractmethod
    def select_sparql(query):
        pass

    @abstractmethod
    def upload_turtle(turtleString, namedGraph):
        pass

    @abstractmethod
    def fetch_namespaces():
        pass


class GraphDBTripleStore(AbstractTripleStore):

    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(endpoint, updateEndpoint=endpoint + '/statements')

        super().__init__()
    
    def fetch_namespaces(self):
        url = self.endpoint + "/namespaces"
        response = requests.get(url, headers={"Accept": "application/sparql-results+json"})

        responseDict = response.json()
        return responseDict["results"]["bindings"]

    def upload_turtle(self, turtleString, namedGraph):
        url = self.endpoint + "/rdf-graphs/service?graph=" + namedGraph
        response = requests.post(url, data=turtleString, headers={"Content-Type": "text/turtle"})
        
        if response.status_code > 299 | response.status_code < 200:
            print("url: " + url)
            print("data: " + turtleString)
            print(response.text)
            raise Exception("Could not upload turtle to RDF endpoint")

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