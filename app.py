# app.py
from flask import Flask
from flask import request
from multiprocessing import Value
from flask import json
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/counter')
def index():
    with counter.get_lock():
        counter.value += 1
    return json.jsonify(counter.value)

if __name__ == '__main__':
    app.run(debug=True)

