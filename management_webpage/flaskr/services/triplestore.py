from abc import ABC, abstractmethod
from turtle import turtles
<<<<<<< HEAD
from urllib import response
=======
>>>>>>> sprint

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

<<<<<<< HEAD
    def __init__(self, server_url, repository_name, create_if_not_exists=False) -> None:
        self.endpoint = server_url + "/repositories/" + repository_name

        if create_if_not_exists:
            self.__create_repo_if_not_exists(server_url, repository_name)

        self.sparql = SPARQLWrapper(self.endpoint, updateEndpoint=self.endpoint + '/statements')

        super().__init__()
    
    def __create_repo_if_not_exists(self, server_url, repository_name):
        url = server_url + "/repositories"
        response = requests.get(url, headers={"Accept": "application/sparql-results+json"})

        repositories = response.json()["results"]["bindings"]
        repoFound = False
        for repository in repositories:
            if repository["id"]["value"] == repository_name:
                repoFound = True
        
        if not repoFound:
            print("repository not found, attempting to create")
            url = server_url + "/rest/repositories"
            repoConfig = f"""
                @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
                @prefix rep: <http://www.openrdf.org/config/repository#> .
                @prefix sail: <http://www.openrdf.org/config/sail#> .
                @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

                <#{repository_name}> a rep:Repository;
                rep:repositoryID "{repository_name}";
                rep:repositoryImpl [
                    rep:repositoryType "graphdb:FreeSailRepository";
                    <http://www.openrdf.org/config/repository/sail#sailImpl> [
                        <http://www.ontotext.com/trree/owlim#base-URL> "http://example.org/owlim#";
                        <http://www.ontotext.com/trree/owlim#check-for-inconsistencies> "false";
                        <http://www.ontotext.com/trree/owlim#defaultNS> "";
                        <http://www.ontotext.com/trree/owlim#disable-sameAs> "false";
                        <http://www.ontotext.com/trree/owlim#enable-context-index> "false";
                        <http://www.ontotext.com/trree/owlim#enable-literal-index> "true";
                        <http://www.ontotext.com/trree/owlim#enablePredicateList> "true";
                        <http://www.ontotext.com/trree/owlim#entity-id-size> "32";
                        <http://www.ontotext.com/trree/owlim#entity-index-size> "10000000";
                        <http://www.ontotext.com/trree/owlim#imports> "";
                        <http://www.ontotext.com/trree/owlim#in-memory-literal-properties> "true";
                        <http://www.ontotext.com/trree/owlim#query-limit-results> "0";
                        <http://www.ontotext.com/trree/owlim#query-timeout> "0";
                        <http://www.ontotext.com/trree/owlim#read-only> "false";
                        <http://www.ontotext.com/trree/owlim#repository-type> "file-repository";
                        <http://www.ontotext.com/trree/owlim#ruleset> "owl2-rl-optimized";
                        <http://www.ontotext.com/trree/owlim#storage-folder> "storage";
                        <http://www.ontotext.com/trree/owlim#throw-QueryEvaluationException-on-timeout> "false";
                        sail:sailType "graphdb:FreeSail"
                        ]
                    ];
                rdfs:label "{repository_name}" .
            """
            data = { "config": repoConfig }
            # header = { "Content-Type": "multipart/form-data" }
            response = requests.post(url, files=data)#, headers=header)
            print(response.text)

=======
    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(endpoint, updateEndpoint=endpoint + '/statements')

        super().__init__()
    
>>>>>>> sprint
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