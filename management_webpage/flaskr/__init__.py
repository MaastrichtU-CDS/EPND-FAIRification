import os

from flask import Flask
import json
from flaskr.services import triplestore

import logging

logging.basicConfig(
     format="%(asctime)s - %(name)-14s - %(levelname)-8s - %(message)s",
     level=logging.DEBUG
)

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
     rdfStore = triplestore.GraphDBTripleStore(app.config.get("graphdb_server"),
                                               app.config.get("repository"),
                                               create_if_not_exists=True,
                                               fill_folder_when_created=app.config.get("turtle_folder"))

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
     if "turtle_folder" in app.config:
          cedar_controller.turtle_folder = app.config.get("turtle_folder")

     from . import data_controller
     app.register_blueprint(data_controller.bp)
     data_controller.rdfStore = rdfStore
     data_controller.triplifierRestUri = app.config.get("triplifier_service")

     from . import publish_controller
     app.register_blueprint(publish_controller.bp)
     publish_controller.rdfStore = rdfStore
     publish_controller.triplifierRestUri = app.config.get("triplifier_service")
     
     return app

#@app.route('/')
#def hello():
#    return redirect("/linkdatasets/linkdatasets/")