
# pip install Flask-PyMongo

from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

# 配置 MongoDB URI
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask_mongo_app"
mongo = PyMongo(app)

@app.route('/')
def index():
    users = mongo.db.users.find()  # 获取所有用户
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # 插入到 MongoDB 中
        mongo.db.users.insert_one({
            'username': username,
            'email': email
        })
        return redirect(url_for('index'))

@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    mongo.db.users.delete_one({'_id': ObjectId(user_id)})  # 根据用户 ID 删除
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
