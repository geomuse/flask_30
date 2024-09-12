from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

# 导入模型
from models import User

@app.route('/')
def index():
    return "Welcome to the Flask database tutorial"

if __name__ == '__main__':
    app.run(debug=True)