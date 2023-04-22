import requests
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

@app.route('/login/', methods = ['GET'])
def index():
    return render_template('login.html')

conn = psycopg2.connect(database = 'service_db',
 user = "postgres", password = "k30042004", 
 host = "localhost", port= "5432")
cursor = conn.cursor()

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return render_template('login.html', message = 'please, fill void space')
    cursor.execute("select * from service.users where login=%s and password=%s", (str(username), str(password)))
    records = list(cursor.fetchall())
    if not records:
        return render_template('login.html', message = 'Please, enter correct data')
            

    return render_template('account.html', full_name = records[0][1],
                            login = records[0][2], password = records[0][3])


