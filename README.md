# FLYOVER

## Introduction

We have build a dockerized Data FAIR-ification tool that takes clinical datasets and converts them into Resource Descriptor Format (RDF). This conversion is done by an application which parses an entire structured table as a simple flattened RDF object. This so-called "Triplifier" tool works with PostGreSQL and CSV tables.

For user data, a new module (data_descriptor) is created where the user can describe their own data and provide us with the metadata, which can then be used to create annotations.

## Components

1. Data_descriptor (For user data)

### 1. Data Descriptor Module
A simple graphical interface tool for helping a local user to describe their own data (in the form of CSV or PostGreSQL). On uploading the data, Triplifier runs and converts this data into RDF triples which is then uploaded to the RDF store, along with an OWL file. The next page displays the list of columns and prompts the user to give some basic information about their data which is then added back to the OWL file in the RDF store.  

#### How to run?
To execute the complete workflow, please execute the following commands from the project folder:
```
docker-compose up -d
```
The end result of the data_descriptor_main.py process in the Data Descriptor module is:

1) An ontology (OWL) file that describes the schema of the structured data but does not contain any data elements in itself, along with the selections and annotations entered by the user through the simple graphical user interface.

2) A Turtle RDF (TTL) file that contains the data elements in term subject-predicate-object sentences.

You can find the following systems:
* Postgres web admin: [[http://localhost/]]
* RDF repository: [[http://localhost:7200]]

#### Publishing anonyous METADATA
The user can publish their OWL files to a private cloud repository, which can then be used to create a customised annotation graph for their data. The usage of metadata for the creation of annotations ensures the privacy of user data.

## Developers

- Varsha Gouthamchand
- Leonard Wee
- Johan van Soest


