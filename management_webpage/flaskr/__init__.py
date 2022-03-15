from flask import Flask, render_template, request, flash

app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hi there!"

if (__name__ == "__main__"):
     app.run(host='0.0.0.0', port=5000)

from . import  linkdatasets
app.register_blueprint(linkdatasets.bp)