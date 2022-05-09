import os

from flask import Flask

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
     app.config.from_mapping(
          SECRET_KEY='dev',
          DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
     )

     if test_config is None:
        # Load the instance config, if it exists, when not testing
          app.config.from_pyfile('config.py', silent=True)
     else:
        # Load the test config if passed in
          app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
     try:
          os.makedirs(app.instance_path)
     except OSError:
          pass

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