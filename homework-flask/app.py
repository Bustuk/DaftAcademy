from flask import Flask
from flask import request
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/method', methods=['GET',"POST","PUT","DELETE"])
def request_info():
    return f"{request.method}"

@app.route("/show_data", methods=["POST"])
def print_json():
    data=request.get_json()
    string=str(data)
    string = string.replace('\'', '\"')
    return string

@app.route('/pretty_print_name', methods=["POST"])
def print():
    data = request.get_json()
    name=str(data["name"])
    surname=str(data["surename"])
    string=f'Na imię mu {name}, a nazwisko jego {surname}'
    return string

number = 0

@app.route('/counter')
def index():
    global number
    number += 1
    return str(number)

if __name__ == '__main__':
    app.run(debug=True)

