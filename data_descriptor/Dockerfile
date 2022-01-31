from python:3.9

USER root

RUN apt-get update -y && \
    apt-get install -y openjdk-11-jdk && \
	apt-get clean && rm -rf var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64 #This can vary
ENV PATH $PATH:$JAVA_HOME/bin

ENV POST_URL https://jdbc.postgresql.org/download/postgresql-42.2.5.jar
RUN wget ${POST_URL}


WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./ /app/
CMD python3 data_descriptor_main.py