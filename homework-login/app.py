from functools import wraps
from uuid import uuid4, UUID

from flask import Flask, request, Response, session, redirect, url_for, jsonify
from jinja2 import Template


app = Flask(__name__)
app.secret_key = bytes.fromhex(
    'dfba670ebc21410076bb5941140e789ac6342e09c18da920'
)


@app.route('/')
def root():
    return 'Hello, World!'


def check_auth(username, password):
    """This function is called to check if a username password combination is
    valid."""
    return username == 'TRAIN' and password == 'TuN3L'


def please_authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_basic_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return please_authenticate()
        return func(*args, **kwargs)

    return wrapper


@app.route('/login/', methods=['GET', 'POST'])
@requires_basic_auth
def login():
    session['username'] = request.authorization.username
    return redirect('/hello')


def requires_user_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            return redirect('/login/')
        return func(*args, **kwargs)

    return wrapper
template = Template('<p id="greeting"> Hello, {{user}}!</p>')

@app.route('/hello')
@requires_user_session
def hello():
    x=session['username']
    render = template.render(user=str(x))
    return render
    #return str(x) #f"<h1 id='greeting'>Hello, {{ session['username'] }}!</h1>"
    #render_template('greeting.html', name=session['username'])


@app.route('/logout/', methods=['GET', 'POST'])
@requires_user_session
def logout():
    if request.method == 'GET':
        return redirect('/')
    del session['username']
    return redirect('/')





if __name__ == '__main__':
    app.run(debug=True, use_debugger=False)
