import getpass, time

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from data import Environmentals

#TODO: Install mysql on rpi: sudo apt-get install mysql-server libmysqlclient-dev

app = Flask(__name__)
app.config['MySQL_HOST'] = 'localhost'
app.config['MySQL_USER'] = 'root'
app.config['MySQL_PASSWORD'] = getpass.getpass()
app.config['MySQL_DB'] = 'users'
app.config['MySQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


Environmentals = Environmentals()


def get_divs():
    Divs = dict()

    if Environmentals['ctemp'] >= 18.0 and Environmentals['ctemp'] <= 25.0:
        Divs['ctemp'] = "alert alert-success"
    elif Environmentals['ctemp'] < 18.0 and Environmentals['ctemp'] >= 16.0:
        Divs['ctemp'] = "alert alert-warning"
    else:
        Divs['ctemp'] = "alert alert-danger"

    if Environmentals['htemp'] >= 28.0 and Environmentals['htemp'] <= 38.0:
        Divs['htemp'] = "alert alert-success"
    elif Environmentals['htemp'] < 28.0 and Environmentals['htemp'] >= 26.0:
        Divs['htemp'] = "alert alert-warning"
    else:
        Divs['htemp'] = "alert alert-danger"

    if Environmentals['uv'] >= 7 and Environmentals['uv'] <= 11:
        Divs['uv'] = "alert alert-success"
    elif Environmentals['uv'] < 7 and Environmentals['uv'] >= 5:
        Divs['uv'] = "alert alert-warning"
    else:
        Divs['uv'] = "alert alert-danger"

    if Environmentals['chum'] >= 28.0 and Environmentals['chum'] <= 38.0:
        Divs['chum'] = "alert alert-success"
    elif Environmentals['chum'] < 28.0 and Environmentals['chum'] >= 26.0:
        Divs['chum'] = "alert alert-warning"
    else:
        Divs['chum'] = "alert alert-danger"

    if Environmentals['hhum'] >= 28.0 and Environmentals['hhum'] <= 38.0:
        Divs['hhum'] = "alert alert-success"
    elif Environmentals['hhum'] < 28.0 and Environmentals['hhum'] >= 26.0:
        Divs['hhum'] = "alert alert-warning"
    else:
        Divs['hhum'] = "alert alert-danger"

    return Divs


@app.route('/')
def home():
    Divs = get_divs()
    Environmentals['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.gmtime())
    return render_template('home.html', environmentals=Environmentals, divs=Divs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

    return render_template('login.html', form=form)


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


if __name__ == '__main__':
    app.run(host='192.168.0.5', debug=True)
