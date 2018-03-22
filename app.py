import getpass, time

from functools import wraps
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from data import Environmentals

#TODO: Install mysql on rpi: sudo apt-get install mysql-server libmysqlclient-dev

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'focusRITE339'
app.config['MYSQL_DB'] = 'hectormon'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


Environmentals = Environmentals()


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You do not have permission to do that.', 'danger')
            return redirect(url_for('login'))
    return wrap


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
@is_logged_in
def dashboard():
    Divs = get_divs()
    Environmentals['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.gmtime())
    return render_template('dashboard.html', environmentals=Environmentals, divs=Divs)


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                cur.close()
                return redirect(url_for('dashboard'))
            else:
                error = 'Incorrect password'
                cur.close()
                return render_template('login.html', error=error, form=form)

        else:
            error = 'Username not found: {0}'.format(username)
            cur.close()
            return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(host='192.168.0.5', debug=True)
