from flask import Flask, request, render_template
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

def send_mail(message):
    try:
        # 构造邮件
        msg = MIMEText(message)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # 从表单获取数据
        email = request.form['email']
        send_mail(email)
        return render_template('result.html')
    else:
        return "Please use the form to submit data."

if __name__ == '__main__':

    app.run(debug=True)