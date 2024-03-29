from abc import ABC, abstractmethod
from urllib import response

from SPARQLWrapper import SPARQLWrapper, JSON, GET, POST, POSTDIRECTLY
import requests
import glob
import os

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
    
    def get_values_from_results(self, results):
        returnData = [ ]
        colNames = None
        for result in results:
            if colNames is None:
                colNames = result.keys()

            returnRow = {}
            for colName in colNames:
                returnRow[colName] = result[colName]['value']
            
            returnData.append(returnRow)
        return returnData


class GraphDBTripleStore(AbstractTripleStore):

    def __init__(self, server_url, repository_name, create_if_not_exists=False, fill_folder_when_created=None) -> None:
        self.endpoint = server_url + "/repositories/" + repository_name

        if create_if_not_exists:
            repo_created = self.__create_repo_if_not_exists(server_url, repository_name)

            if (repo_created) & (fill_folder_when_created is not None):
                self.__load_turtle_from_folder(fill_folder_when_created)

        self.sparql = SPARQLWrapper(self.endpoint, updateEndpoint=self.endpoint + '/statements')

        super().__init__()
    
    def __load_turtle_from_folder(self, folder_name):
        found_files = glob.glob(os.path.join(folder_name, "**", "*.ttl"), recursive=True)
        for found_file in found_files:
            head, tail = os.path.split(found_file)
            with open(found_file) as f:
                turtleString = f.read()
                self.upload_turtle(turtleString, f"http://{tail}.local/")
    
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
                        <http://www.ontotext.com/trree/owlim#disable-sameAs> "true";
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
                        <http://www.ontotext.com/trree/owlim#ruleset> "rdfsplus-optimized";
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
            if response.status_code >= 200 & response.status_code < 300:
                return True
        
        return False

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
