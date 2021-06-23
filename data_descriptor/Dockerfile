FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev libpq-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python3", "data_descriptor_main.py"]