from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['recipe']
collection = db['info']

r = [ recipe for recipe in collection.find() ]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',name='geo',content=r)

if __name__ == '__main__':

    app.run(debug=True)