# docker-compose up -d

# echo "Waiting for GraphDB to be up-and-running"
# curl -X GET --header 'Accept: application/json' 'http://localhost:7200/rest/locations'
# retVal=$?
# while [ $retVal -ne 0 ]
# do
#     sleep 5
#     curl -X GET --header 'Accept: application/json' 'http://localhost:7200/rest/locations'
#     retVal=$?
# done

# # Create repository from config
# curl -X POST -F config=@config.ttl --header 'Content-Type: multipart/form-data' --header 'Accept: */*' 'http://localhost:7200/rest/repositories'

# Upload SHACL file
sed "s/#.*$//g" ../shapeTest/shacl.ttl > shacl.ttl
curl -d @shacl.ttl --header "Content-Type: application/x-turtle" http://localhost:7200/repositories/epnd_dummy/statements?context=%3Chttp://shacl.local/%3E
rm shacl.ttl

# Upload ontology file
curl -d @ontology.owl --header "Content-Type: application/rdf+xml" http://localhost:7200/repositories/epnd_dummy/statements?context=%3Chttp://ontology.local/%3E

# Upload data file
curl -d @output.ttl --header "Content-Type: application/x-turtle" http://localhost:7200/repositories/epnd_dummy/statements?context=%3Chttp://data.local/%3E