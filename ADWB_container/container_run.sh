#! /bin/bash

/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=/opt/graphdb/home -Dorg.xml.sax.driver=com.sun.org.apache.xerces.internal.parsers.SAXParser -Djdk.xml.entityExpansionLimit=1000000 & > /graphdb_stdout.log 2> /graphdb_stderr.log
sleep 60

cd /triplifier-boot && java -jar triplifier-boot.jar & > /triplifier_stdout.log 2> /triplifier_stderr.log
cd /app

sleep 20

# Set triplifier location
python replace_env.py

sleep 5

FLASK_APP=flaskr
FLASK_ENV=development
export FLASK_APP=$FLASK_APP
export FLASK_ENV=$FLASK_ENV
flask run -h 0.0.0.0 -p 5000