FROM python:3.8-bullseye

RUN apt update && apt upgrade -y
RUN apt install -y nodejs npm

ADD ./ /app
EXPOSE 5000
WORKDIR /app

RUN cd cedar_embeddable_editor && sh build_frontend.sh

RUN pip install -r requirements.txt

CMD ["sh", "run.sh"]