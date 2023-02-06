FROM ghcr.io/maastrichtu-cds/fair_tools_docker-graphdb/docker-graphdb:latest
#FROM jvsoest/graphdb

RUN apt update && apt upgrade -y
# Install Python
RUN apt install -y python3 python3-pip build-essential libssl-dev libffi-dev python3-dev python-is-python3

# Install NodeJS
RUN curl -sL https://deb.nodesource.com/setup_16.x -o /tmp/nodesource_setup.sh
RUN bash /tmp/nodesource_setup.sh
RUN apt install -y nodejs

# Upload and configure management application
ADD ./app /app
WORKDIR /app

RUN cd cedar_embeddable_editor && bash build_frontend.sh
RUN pip install -r requirements.txt

WORKDIR /

## Install triplifier-boot
RUN mkdir /triplifier-boot
COPY triplifier/triplifier-boot-0.0.1-SNAPSHOT.jar /triplifier-boot/triplifier-boot.jar

## Add run file
COPY container_run.sh /run.sh
COPY replace_env.py /replace_env.py

WORKDIR /
EXPOSE 5000 7200 8080
ENTRYPOINT ["/bin/bash", "run.sh"]
CMD [""]