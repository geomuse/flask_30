---
layout: post
title:  11/30-Flask-WTF
date:   2024-09-14 11:24:29 +0800
categories: 
    - python 
    - flask
    - challenge
---

这是一个使用 `Flask-WTF` 创建用户注册和登录表单的示例。代码分为三个部分：表单模型、视图函数、以及HTML模板文件。

### 1. 表单模型（forms.py）
使用 `Flask-WTF` 来定义表单，并进行验证。

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from your_project.models import User  # 引入 User 模型以检查是否有重复用户名或邮箱

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # 自定义验证函数，确保用户名或邮箱未被占用
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    submit = SubmitField('Login')
```

### 2. 视图函数（routes.py）
创建视图函数来处理表单提交及验证。

```python
from flask import render_template, url_for, flash, redirect
from your_project import app, db, bcrypt
from your_project.forms import RegistrationForm, LoginForm
from your_project.models import User
from flask_login import login_user, logout_user

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # 密码加密
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # 创建用户
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        # 保存到数据库
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 查找用户
        user = User.query.filter_by(email=form.email.data).first()
        # 验证用户和密码
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
```

### 3. HTML模板文件

#### register.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
</head>
<body>
    <h2>Register</h2>
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <div>
            {{ form.username.label }} {{ form.username(size=32) }}
        </div>
        <div>
            {{ form.email.label }} {{ form.email(size=32) }}
        </div>
        <div>
            {{ form.password.label }} {{ form.password(size=32) }}
        </div>
        <div>
            {{ form.confirm_password.label }} {{ form.confirm_password(size=32) }}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
</body>
</html>
```

#### login.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="POST" action="">
        {{ form.hidden_tag() }}
        <div>
            {{ form.email.label }} {{ form.email(size=32) }}
        </div>
        <div>
            {{ form.password.label }} {{ form.password(size=32) }}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
</body>
</html>
```

### 4. 数据库模型（models.py）
确保你有一个 `User` 模型来保存用户数据。

```python
from your_project import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
```

### 5. 配置（config.py）
别忘了在你的 `config.py` 中设置一个 `SECRET_KEY` 和数据库 URI。

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
```

这是一个完整的 Flask 用户注册与登录表单的示例，使用了 `Flask-WTF` 进行表单验证，并将用户信息存储在数据库中。