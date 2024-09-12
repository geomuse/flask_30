# config.py

import os

class Config:
    MAIL_SERVER = 'smtp.gmail.com'  # 邮件服务器地址
    MAIL_PORT = 587  # 端口号
    MAIL_USE_TLS = True  # 启用TLS
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # 发件人邮箱
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # 发件人邮箱的密码或App密码
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')  # 默认发件人

from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config.Config')  # 从配置文件加载配置

mail = Mail(app)  # 初始化 Flask-Mail

from flask_mail import Message
from flask import Flask, render_template

# 发送邮件的函数
@app.route('/send_email')
def send_email():
    msg = Message('Hello from Flask-Mail',  # 主题
                  recipients=['recipient@example.com'])  # 收件人
    msg.body = 'This is a test email sent from Flask-Mail.'  # 邮件正文
    msg.html = '<h1>This is a test email sent from Flask-Mail</h1>'  # HTML格式的正文

    try:
        mail.send(msg)  # 发送邮件
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

...