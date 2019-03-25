# app.py
from flask import Flask
from flask import request
from flask import redirect
from flask_basicauth import BasicAuth

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'TRAIN'
app.config['BASIC_AUTH_PASSWORD'] = 'TuN3L'

basic_auth = BasicAuth(app)


@app.route('/login', methods=['POST'])
@basic_auth.required
def secret_view():
    return redirect('/hello')

@app.route("/hello")
def html():
    return "o kurka"

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/counter')
def index():
    return "SIALAALALA"


if __name__ == '__main__':
    app.run(debug=True)

