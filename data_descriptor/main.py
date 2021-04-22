
from flask import Flask, render_template, request, flash
import os
import csv
import pandas as pd
from psycopg2 import sql, connect
import json
import subprocess
import re
import requests
import shutil

app = Flask(__name__)

app.secret_key = "secret_key"

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
file_path = None
table = None
url = None
username = None
password = None
db_name = None
conn = None
col_cursor = None
csvPath = False
mydict = {}
uploaded_file = None

# Root URL
@app.route('/')
def index():
    global file_path
    file_path = None
    global table
    table = None
    global url
    url = None
    global username
    username = None
    global password
    password = None
    global db_name
    db_name = None
    global conn
    conn = None
    global col_cursor
    col_cursor = None
    global csvPath
    csvPath = False
    global mydict
    mydict = {}
    global uploaded_file
    uploaded_file = None
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')

def allowed_log_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['csv']

# Get the uploaded files
@app.route("/csv", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      global file_path
      global csvPath
      global uploaded_file

      if not request.files:
          flash('No file selected for uploading!')
          return render_template('index.html')
      uploaded_file = request.files['file']

      if uploaded_file.filename == '':
          flash('No file selected for uploading!')
          return render_template('index.html')

      if uploaded_file and allowed_log_file(uploaded_file.filename):
          file_path = os.path.join(app.config['UPLOAD_FOLDER'], "data.csv")
          # set the file path
          uploaded_file.save(file_path)
          columns = getColumns(file_path)
          csvPath = True
          return render_template('categories.html', variable=columns)

      else:
          flash('The only allowed file type is CSV!')
          return render_template('index.html')

def getColumns(csvfile):
    # get the column names
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        i = next(reader)
        return i

@app.route("/postgres", methods=['POST'])
def getCredentials():
      global url, db_name, password, username, table, conn
      username = request.form.get('username')
      password = request.form.get('password')
      url= request.form.get('POSTGRES_URL')
      db_name = request.form.get('POSTGRES_DB')
      table = request.form.get('table')

      try:
          # declare a new PostgreSQL connection object
          conn = connect(
              dbname=db_name,
              user=username,
              host=url,
              password=password
          )

          # print the connection if successful
          print("Connection:", conn)

      except Exception as err:
          print("connect() ERROR:", err)
          conn = None
          flash('Connection unsuccessful. Please check your details!')
          return render_template('index.html')

      columns = get_columns_names(conn, table)

      return render_template('categories.html', variable = columns)

def get_columns_names(conn, table):

    columns = []
    global col_cursor

    # declare cursor objects from the connection
    col_cursor = conn.cursor()

    # concatenate string for query to get column names
    # SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'some_table';
    col_names_str = "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE "
    col_names_str += "table_name = '{}';".format(table)

    # print the SQL string
    #print(col_names_str)

    try:
        sql_object = sql.SQL(
            col_names_str
        ).format(
            sql.Identifier(table)
        )

        # execute the SQL string to get list with col names in a tuple
        col_cursor.execute(sql_object)

        # get the tuple element from the liast
        col_names = (col_cursor.fetchall())
        #print(col_names)
        # iterate list of tuples and grab first element
        for tup in col_names:
            # append the col name string to the list
            columns += [tup[0]]

        # close the cursor object to prevent memory leaks
        col_cursor.close()

    except Exception as err:
        print("get_columns_names ERROR:", err)

    # return the list of column names
    return columns

@app.route("/units", methods=['POST'])
def units():
    global mydict
    conList = []
    f = open('python_output.json', 'w')
    for key in request.form:
         if not re.search("^ncit_comment_", key):
             mydict[key] = {}
             value = request.form.get(key)
             ncit = request.form.get('ncit_comment_'+key)
             comment = request.form.get('comment_'+key)
             mydict[key]['type'] = value
             mydict[key]['description'] = ncit
             mydict[key]['comments'] = comment
             if value == 'Categorical Nominal' or value == 'Categorical Ordinal':
                 cat = getCategories(key, value)
                 mydict[key]['categories'] = cat
             elif value == 'Continuous':
                 conList.append(key)

    return render_template('units.html', variable = conList)

def getCategories(key, value):

    if (csvPath == True):
         demo_data = pd.read_csv(file_path)
         x = demo_data[key].value_counts()
         y = x.to_dict()
         return y

    else:
        columns = []
        sqlQuery = "select \"{0}\", count(*) from \"{1}\" " .format(key, table)
        sqlQuery += "group by \"{}\";" .format(key)
        #print(sqlQuery)
        sql_object = sql.SQL(sqlQuery).format(sql.Identifier(table))
        #print(sql_object)
        col_cursor = conn.cursor()
        # execute the SQL string to get list with col names in a tuple
        col_cursor.execute(sql_object)

        # get the tuple element from the liast
        col_count = (col_cursor.fetchall())
        # print(col_count)

        # close the cursor object to prevent memory leaks
        col_cursor.close()
        counts = dict((x, y) for x, y in col_count)
        return counts

@app.route("/end", methods=['POST'])
def unitNames():
    #items = getColumns(file_path)
    for key in request.form:
        unitValue = request.form.get(key)
        if unitValue!= "":
            mydict[key]['units'] = unitValue

    jsonObj = json.dumps(mydict, indent= 4)
    f = open('python_output.json', 'a')
    f.write(jsonObj)
    f.close()
    #delete existing JSON output
    if os.path.exists("static/files/python_output.json"):
        os.remove("static/files/python_output.json")
    else:
        print("The file does not exist")
    #move new JSON output to static/files
    shutil.move("python_output.json", "static/files/python_output.json")
    #delete existing output and OWL files
    if os.path.exists("static/files/ontology.owl"):
        os.remove("static/files/ontology.owl")
    else:
        print("The file does not exist")

    if os.path.exists("static/files/output.ttl"):
        os.remove("static/files/output.ttl")
    else:
        print("The file does not exist")
    #initialize Triplifier
    initTriples()
    #fileupload()
    return render_template('success.html')

def initTriples():

    try:
        if (csvPath == True):
            args1 = "java -jar javaTool/triplifier-1.0-SNAPSHOT-jar-with-dependencies.jar -p javaTool/triplifier.properties"
            #print(args1)
            subprocess.call(args1, shell=True)
        else:
            f = open("javaTool//triplifierSQL.properties", "w")
            f.write("jdbc.url = jdbc:postgresql://localhost/" +db_name+"\njdbc.user = " +username+ "\njdbc.password = " +password+ "\njdbc.driver = org.postgresql.Driver")
            f.close()
            args2 = "java -jar javaTool/triplifier-1.0-SNAPSHOT-jar-with-dependencies.jar -p javaTool/triplifierSQL.properties"
            subprocess.call(args2, shell=True)

        shutil.move("ontology.owl", "static/files/ontology.owl")
        shutil.move("output.ttl", "static/files/output.ttl")

    except Exception as err:
        print(err)

if (__name__ == "__main__"):
     app.run(port = 5000)