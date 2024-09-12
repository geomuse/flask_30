from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# 配置 MongoDB 客户端
client = MongoClient('mongodb://localhost:27017/')
db = client.flask_mongo_app  # 选择数据库
users_collection = db.users  # 选择集合

@app.route('/')
def index():
    users = users_collection.find()  # 获取所有用户
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # 插入到 MongoDB 中
        users_collection.insert_one({
            'username': username,
            'email': email
        })
        return redirect(url_for('index'))

@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    users_collection.delete_one({'_id': ObjectId(user_id)})  # 根据用户 ID 删除
    return redirect(url_for('index'))

if __name__ == '__main__':
    
    app.run(debug=True)
