#! /bin/bash

/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=/opt/graphdb/home -Dorg.xml.sax.driver=com.sun.org.apache.xerces.internal.parsers.SAXParser -Djdk.xml.entityExpansionLimit=1000000 & > /graphdb_stdout.log 2> /graphdb_stderr.log
sleep 60

cd /triplifier-boot && java -jar triplifier-boot.jar & > /triplifier_stdout.log 2> /triplifier_stderr.log
cd /app

# Set triplifier location
if [ -z "$TRIPLIFIER_LOCATION" ]; then
    TRIPLIFIER_LOCATION=$(cat /app/config.json | jq '.triplifier_service')
    export TRIPLIFIER_LOCATION
fi
cat /app/config.json | jq --argjson "triplifier_location" "$TRIPLIFIER_LOCATION" '.triplifier_service = $triplifier_location' > /app/config.json

FLASK_APP=flaskr
FLASK_ENV=development
export FLASK_APP=$FLASK_APP
export FLASK_ENV=$FLASK_ENV
flask run -h 0.0.0.0 -p 5000