import os

from flask import Flask
import json

#app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hi there!"

#if (__name__ == "__main__"):
#     app.run(host='0.0.0.0', port=5000)



def create_app(test_config=None):
     app = ...
    # Create and configure the app
     app = Flask(__name__, instance_relative_config=True)
     # app.config.from_mapping(
     #      SECRET_KEY='dev',
     #      DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
     # )

     # Load the instance config, if exists
     print("loading JSON config")
     with open("config.json") as f:
          app.config.update(json.load(f))

     from . import linkdatasets
     app.register_blueprint(linkdatasets.bp)
     app.add_url_rule('/', endpoint='linker')

     from . import mapDatasets
     app.register_blueprint(mapDatasets.bp)
     app.add_url_rule('/', endpoint='mapper')


     
     return app

#@app.route('/')
#def hello():
#    return redirect("/linkdatasets/linkdatasets/")