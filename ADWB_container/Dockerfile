#FROM registry.gitlab.com/um-cds/fair/tools/docker-graphdb:latest
FROM jvsoest/graphdb

RUN apt update && apt upgrade -y
# Install Python
RUN apt install -y python3 python3-pip build-essential libssl-dev libffi-dev python3-dev python-is-python3
# Install NodeJS
RUN apt install -y nodejs npm

# Upload and configure management application
ADD ./app /app
WORKDIR /app

RUN cd cedar_embeddable_editor && sh build_frontend.sh
RUN pip install -r requirements.txt

WORKDIR /

# Start instruction GraphDB
RUN echo "/opt/graphdb/dist/bin/graphdb -Dgraphdb.home=/opt/graphdb/home -Dorg.xml.sax.driver=com.sun.org.apache.xerces.internal.parsers.SAXParser -Djdk.xml.entityExpansionLimit=1000000 & > /graphdb_stdout.log 2> /graphdb_stderr.log" >> run.sh

# Start instruction management webpage
RUN echo "cd /app" >> run.sh && \
    echo "source venv/bin/activate" >> run.sh && \
    echo "FLASK_APP=flaskr" >> run.sh && \
    echo "FLASK_ENV=development" >> run.sh && \
    echo "export FLASK_APP=$FLASK_APP" >> run.sh && \
    echo "export FLASK_ENV=$FLASK_ENV" >> run.sh && \
    echo "flask run -h 0.0.0.0 -p 5000" >> run.sh

WORKDIR /
EXPOSE 5000 7200
ENTRYPOINT ["sh run.sh"]
CMD [""]
