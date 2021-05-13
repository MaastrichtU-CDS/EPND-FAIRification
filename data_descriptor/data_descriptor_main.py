
from flask import Flask, render_template, request, flash
import os
import csv
import pandas as pd
from psycopg2 import sql, connect
import json
import subprocess
import re
import shutil

app = Flask(__name__)
app.secret_key = "secret_key"
# enable debugging mode
app.config["DEBUG"] = True
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Cache:
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

v = Cache()

# Root URL
@app.route('/')
def index():
     # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')

def allowed_log_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['csv']

# Get the uploaded files
@app.route("/csv", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      if not request.files:
          flash('No file selected for uploading!')
          return render_template('index.html')
      v.uploaded_file = request.files['file']

      if v.uploaded_file.filename == '':
          flash('No file selected for uploading!')
          return render_template('index.html')

      if v.uploaded_file and allowed_log_file(v.uploaded_file.filename):
          v.file_path = os.path.join(UPLOAD_FOLDER, "data.csv")
          # set the file path
          v.uploaded_file.save(v.file_path)
          columns = getColumns(v.file_path)
          v.csvPath = True
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
      v.username = request.form.get('username')
      v.password = request.form.get('password')
      v.url= request.form.get('POSTGRES_URL')
      v.db_name = request.form.get('POSTGRES_DB')
      v.table = request.form.get('table')

      try:
          # declare a new PostgreSQL connection object
          v.conn = connect(
              dbname=v.db_name,
              user=v.username,
              host=v.url,
              password=v.password
          )

          # print the connection if successful
          print("Connection:", v.conn)

      except Exception as err:
          print("connect() ERROR:", err)
          conn = None
          flash('Connection unsuccessful. Please check your details!')
          return render_template('index.html')

      columns = get_columns_names(v.conn, v.table)

      return render_template('categories.html', variable = columns)

def get_columns_names(conn, table):

    columns = []

    # declare cursor objects from the connection
    v.col_cursor = conn.cursor()

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

        # evecute the SQL string to get list with col names in a tuple
        v.col_cursor.execute(sql_object)

        # get the tuple element from the liast
        col_names = (v.col_cursor.fetchall())
        #print(col_names)
        # iterate list of tuples and grab first element
        for tup in col_names:
            # append the col name string to the list
            columns += [tup[0]]

        # close the cursor object to prevent memory leaks
        v.col_cursor.close()

    except Exception as err:
        print("get_columns_names ERROR:", err)

    # return the list of column names
    return columns

@app.route("/units", methods=['POST'])
def units():
    conList = []
    f = open('python_output.json', 'w')
    for key in request.form:
         if not re.search("^ncit_comment_", key):
             v.mydict[key] = {}
             value = request.form.get(key)
             ncit = request.form.get('ncit_comment_'+key)
             comment = request.form.get('comment_'+key)
             v.mydict[key]['type'] = value
             v.mydict[key]['description'] = ncit
             v.mydict[key]['comments'] = comment
             if value == 'Categorical Nominal' or value == 'Categorical Ordinal':
                 cat = getCategories(key, value)
                 v.mydict[key]['categories'] = cat
             elif value == 'Continuous':
                 conList.append(key)

    return render_template('units.html', variable = conList)

def getCategories(key, value):

    if (v.csvPath == True):
         demo_data = pd.read_csv(v.file_path)
         x = demo_data[key].value_counts()
         y = x.to_dict()
         return y

    else:
        columns = []
        sqlQuery = "select \"{0}\", count(*) from \"{1}\" " .format(key, v.table)
        sqlQuery += "group by \"{}\";" .format(key)
        #print(sqlQuery)
        sql_object = sql.SQL(sqlQuery).format(sql.Identifier(v.table))
        #print(sql_object)
        v.col_cursor = v.conn.cursor()
        # evecute the SQL string to get list with col names in a tuple
        v.col_cursor.execute(sql_object)

        # get the tuple element from the liast
        col_count = (v.col_cursor.fetchall())
        # print(col_count)

        # close the cursor object to prevent memory leaks
        v.col_cursor.close()
        counts = dict((x, y) for x, y in col_count)
        return counts

@app.route("/end", methods=['POST'])
def unitNames():
    #items = getColumns(file_path)
    for key in request.form:
        unitValue = request.form.get(key)
        if unitValue!= "":
            v.mydict[key]['units'] = unitValue

    jsonObj = json.dumps(v.mydict, indent= 4)
    f = open('python_output.json', 'a')
    f.write(jsonObj)
    f.close()
    # move new JSON output
    shutil.move("python_output.json", "JSON_Output/python_output.json")
    #initialize Triplifier
    initTriples()
    #fileupload()
    return render_template('success.html')

def initTriples():

    try:
        if (v.csvPath == True):
            f = open("triplifierCSV.properties", "w")
            f.write("jdbc.url = jdbc:relique:csv:static//files?fileExtension=.csv\njdbc.user = \njdbc.password = \njdbc.driver = org.relique.jdbc.csv.CsvDriver"
                    "\n\nrepo.type = rdf4j\nrepo.url = http://rdf-store:7200\nrepo.id = "+os.path.splitext(str(v.uploaded_file.filename))[0])
            f.close()
            args1 = "docker run --rm ^ -v %cd%/output.ttl:/output.ttl ^" \
                    "-v %cd%/ontology.owl:/ontology.owl ^" \
                    "-v %cd%/triplifierCSV.properties:/triplifier.properties ^" \
                    "registry.gitlab.com/ud-cds/fair/tools/triplifier:1.0.0"
            #print(args1)
            subprocess.call(args1, shell=True)
        else:
            #f = open("triplifierSQL.properties", "w")
            #f.write("jdbc.url = jdbc:postgresql://localhost/" +db_name+"\njdbc.user = " +username+ "\njdbc.password = " +password+ "\njdbc.driver = org.postgresql.Driver")
            #f.close()
            args2 = "docker run --rm ^ -v %cd%/output.ttl:/output.ttl ^" \
                    "-v %cd%/ontology.owl:/ontology.owl ^" \
                    "-v %cd%/triplifier_"+v.db_name+".properties:/triplifier.properties ^" \
                    "registry.gitlab.com/ud-cds/fair/tools/triplifier:1.0.0"
            subprocess.call(args2, shell=True)

    except Exception as err:
        print(err)

if (__name__ == "__main__"):
     app.run(port = 5050)