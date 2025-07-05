from flask import Flask, request, abort
import os
import csv
import psycopg2
from werkzeug.utils import secure_filename
from functools import wraps
import sys
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(var_name):
    try:
        return os.environ[var_name].strip()
    except KeyError:
        raise EnvironmentError(f"The environment variable {var_name} is not set.")
    
try:
    USERNAME = get_env_variable('USERNAME_WEBHOOK')
    PASSWORD = get_env_variable('PASSWORD_WEBHOOK')
    HOST_DATABASE = get_env_variable('HOST_DATABASE')
    PORT_DATABASE = get_env_variable('PORT_DATABASE')
    DATABASE = get_env_variable('DATABASE')
    USER_DATABASE = get_env_variable('USER_DATABASE')
    PASSWORD_DATABASE = get_env_variable('PASSWORD_DATABASE')

except KeyError as err:
    print(f"ENV Variable nicht gesetzt: {err}")
    sys.exit(1)

app = Flask(__name__)
UPLOAD_FOLDER = '/code/data'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

USERNAME_AUTH = USERNAME
PASSWORD_AUTH = PASSWORD

def check_auth(username, password):

    return username == USERNAME_AUTH and password == PASSWORD_AUTH

def authenticate():
    return abort(401)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

#////********** GET ***********////

@app.route('/webhook', methods=['GET'])
def index():

    return ('********** Das ist eine website. :-)  *********', 200, None)

#//*************** POST ***********///
@app.route('/webhook', methods=['POST'])
@requires_auth
def receive_report():
#    if 'file' not in request.files:
#        return 'No file part', 400
#
#    file = request.files['file']
#    filename = secure_filename(file.filename)
#    filepath = os.path.join(UPLOAD_FOLDER, filename)
#    file.save(filepath)
#   
#   print(filepath)
    print("OK")
 #   save_to_db(filepath)
    return 'Datei gespeichert und in die Datenbank importiert', 200



#####//*********** Daten Bank ******/////#############

def save_to_db(csv_path):
    conn = psycopg2.connect(
        host=HOST_DATABASE,
        port=PORT_DATABASE,
        database=DATABASE,
        user=USER_DATABASE,
        password=PASSWORD_DATABASE
    )
    cur = conn.cursor()

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT INTO webhook (
                    TEST1, TEST2, Test3
                    
                ) VALUES (%s, %s, %s)
            """, (
                
                row["TEST1"],
                float(row["TEST2"]),
                int(row["TEST3"]),
                
            ))


    conn.commit()
    cur.close()
    conn.close()
    print(" Die Daten wurden im Datenbank gespeichern ✔")

if __name__ == '__main__':
    app.run(debug=True)
