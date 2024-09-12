from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # 数据传递给模板
    return render_template('index.html', name="geo",
                            age=28 , content=str(pd.read_csv('content.txt')))

if __name__ == '__main__':

    app.run(debug=True)