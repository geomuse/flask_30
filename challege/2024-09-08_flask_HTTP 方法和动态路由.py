from flask import Flask, request, render_template_string

app = Flask(__name__)

# 简单的 HTML 表单
html_form = '''
    <form method="POST">
        <label for="name">Name:</label>
        <input type="text" name="name" id="name">
        <input type="submit" value="Submit">
    </form>
'''

# 动态路由，接受 URL 中的 <name> 参数
@app.route('/user/<name>')
def greet_user(name):
    return f"Hello, {name}!"

@app.route('/submit', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']  # 获取表单提交的 name 字段
        return f"Form submitted with name: {name}"
    return render_template_string(html_form)

if __name__ == "__main__":
    app.run(debug=True)