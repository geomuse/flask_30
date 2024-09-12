from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML 表单的内容作为字符串
form_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Example</title>
</head>
<body>
    <h2>Submit Your Info</h2>
    <form method="POST" action="/submit">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        
        <label for="age">Age:</label>
        <input type="number" id="age" name="age" required><br><br>
        
        <input type="submit" value="Submit">
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(form_html)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # 从表单获取数据
        name = request.form['name']
        age = request.form['age']
        return f"<h1 style='text-align:center;'>Received POST request! Name: {name}, Age: {age}</h1>"
    else:
        return "Please use the form to submit data."

if __name__ == '__main__':
    app.run(debug=True)