# app.py
from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/counter')
def index():
    return "SIALAALALA"


if __name__ == '__main__':
    app.run(debug=True)

