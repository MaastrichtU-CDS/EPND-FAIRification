#curl -X POST --header 'Content-Type: multipart/form-data' --header 'Accept: application/json' -F @config.ttl http://localhost:7200/rest/repositories

curl -d @../shapeTest/shacl.ttl --header "Content-Type: application/x-turtle" http://localhost:7200/repositories/epnd_dummy/statements?context=%3Chttp://shacl.local/%3E

curl -d @ontology.owl --header "Content-Type: application/rdf+xml" http://localhost:7200/repositories/epnd_dummy/statements?context=%3Chttp://ontology.local/%3E

curl -d @output.ttl --header "Content-Type: application/x-turtle" http://localhost:7200/repositories/epnd_dummy/statements?context=%3Chttp://data.local/%3E