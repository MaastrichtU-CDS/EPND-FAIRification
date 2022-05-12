FLASK_APP=flaskr
FLASK_ENV=development

export FLASK_APP=$FLASK_APP
export FLASK_ENV=$FLASK_ENV

flask run -h 0.0.0.0 -p 5000
