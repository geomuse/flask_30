from flask import Flask, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Home Page!"

@app.route('/about')
def about():
    return "This is the about page"

@app.route('/go_home')
def go_home():
    return redirect(url_for('home'))

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    return redirect(url_for('greet', name=name))

@app.route('/greet/<name>')
def greet(name):
    return f"<h1 style='text-align:center;'>Hello, {name}!</h1>"

if __name__ == '__main__':

    app.run(debug=True)