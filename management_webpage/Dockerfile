FROM python:3.8-buster

ADD ./ /app
EXPOSE 5000
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["sh", "run.sh"]