import smtplib
from email.mime.text import MIMEText

"""
# flask 示例
from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.example.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your-email@example.com',
    MAIL_PASSWORD='your-password'
)
mail = Mail(app)

@app.route('/send_mail')
def send_mail():
    msg = Message("Hello",
                  recipients=["to@example.com"],
                  body="This is the email body.")
    mail.send(msg)
    return "Mail sent!"
"""

"""
# smtplib 示例
import smtplib
from email.mime.text import MIMEText

def send_mail():
    msg = MIMEText("This is the email body.")
    msg["Subject"] = "Hello"
    msg["From"] = "your-email@example.com"
    msg["To"] = "to@example.com"

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("your-email@example.com", "your-password")
        server.send_message(msg)

send_mail()
"""

"""
import smtplib
from email.mime.text import MIMEText

def send_mail():
    msg = MIMEText("This is the email body.")
    msg["Subject"] = "Hello"
    msg["From"] = "boonhong565059@gmail.com"
    msg["To"]   = "boonhong565059@gmail.com"

    with smtplib.SMTP("smtp.example.com", 587) as server:
        server.starttls()
        server.login("boonhong565059@gmail.com", "rrapnihjrbasepxd")
        server.send_message(msg)

if __name__ == '__main__' :
    
    send_mail()
"""

import smtplib
from email.mime.text import MIMEText

def send_mail():
    try:
        # 构造邮件
        msg = MIMEText("I\'m geo.")
        msg["Subject"] = "..."
        msg["From"] = "boonhong565059@gmail.com"
        msg["To"] = "boonhong565059@gmail.com"
        
        # 连接 Gmail SMTP 服务器
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()  # 向服务器标识
            server.starttls()  # 启用 TLS 加密
            server.ehlo()
            
            # 使用应用专用密码登录
            server.login("boonhong565059@gmail.com", "rrapnihjrbasepxd")  # 确保16位应用专用密码
            
            # 发送邮件
            server.send_message(msg)
            print("Email sent successfully!")

    except smtplib.SMTPAuthenticationError as e:
        print(f"Authentication failed: {e}")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__' :

    send_mail()
