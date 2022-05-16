import os

from flask import Flask
import json
from flaskr.services import triplestore

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

     # from . import linkdatasets
     # app.register_blueprint(linkdatasets.bp)
     # app.add_url_rule('/', endpoint='linker')
     rdfStore = triplestore.GraphDBTripleStore(app.config.get("rdf_endpoint"))

     from . import mapDatasets
     app.register_blueprint(mapDatasets.bp)
     # app.add_url_rule('/', endpoint='mapper')

     from . import fip_controller
     app.register_blueprint(fip_controller.bp)
     fip_controller.rdfStore = rdfStore

     from . import cedar_controller
     app.register_blueprint(cedar_controller.bp)
     cedar_controller.rdfStore = rdfStore
     if "cedar_instance_base_url" in app.config:
          cedar_controller.cedar_instance_base_url = app.config.get("cedar_instance_base_url")

     
     return app

#@app.route('/')
#def hello():
#    return redirect("/linkdatasets/linkdatasets/")