#FROM registry.gitlab.com/um-cds/fair/tools/docker-graphdb:latest
FROM jvsoest/graphdb

RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-pip build-essential libssl-dev libffi-dev python3-dev python-is-python3

ENTRYPOINT ["/bin/bash"]
CMD [""]
