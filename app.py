import getpass, time

from functools import wraps
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from sensors import toggle_lamp_on, toggle_lamp_off, update_data


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = getpass.getpass()
app.config['MYSQL_DB'] = 'hectormon'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You do not have permission to do that.', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/lamp_on')
@is_logged_in
def lamp_on():
    print 'TURN ON'
    toggle_lamp_on()
    return redirect(url_for('dashboard'))


@app.route('/lamp_off')
@is_logged_in
def lamp_off():
    toggle_lamp_off()
    return redirect(url_for('dashboard'))


@app.route('/update')
def update():
    return redirect(url_for('dashboard'))


def get_div(ref, low, mid, high):
    if ref >= mid and ref <= high:
        return "alert alert-success"
    elif ref < mid and ref >= low:
        return "alert alert-warning"
    else:
        return "alert alert-danger"


def get_divs(Environmentals):
    Divs = dict()

    if Environmentals['parity']:
        Divs['ctemp'] = get_div(float(Environmentals['ctemp']), 15.0, 18.0, 28.0)
        Divs['htemp'] = get_div(float(Environmentals['htemp']), 26.0, 28.0, 39.0)
        Divs['uv'] = get_div(int(Environmentals['uv']), 3, 5, 11)
        Divs['chum'] = get_div(float(Environmentals['chum']), 15.0, 20.0, 50.0)
        Divs['hhum'] = get_div(float(Environmentals['hhum']), 15.0, 20.0, 50.0)

        return Divs

    else:
        return { 'ctemp': "alert alert-danger",
                 'htemp': "alert alert-danger",
                 'chum': "alert alert-danger",
                 'hhum': "alert alert-danger",
                 'uv': "alert alert-danger"
               }


@app.route('/')
@is_logged_in
def dashboard():
    Environmentals = update_data()
    Environmentals['timestamp'] = time.strftime("%b %d %Y %H:%M:%S", time.localtime())
    Divs = get_divs(Environmentals)

    if Environmentals['parity']:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sensordata(ctemp, htemp, chum, hhum, uv) VALUES(%s, %s, %s, %s, %s);", [Environmentals['ctemp'], Environmentals['htemp'], Environmentals['chum'], Environmentals['hhum'], Environmentals['uv']])
        mysql.connection.commit()
        cur.close()
        return render_template('dashboard.html', environmentals=Environmentals, divs=Divs)
    else:
        flash('Unable to read from sensors. Refresh page and try again. If unsuccessful check sensor connection.', 'danger')
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
    app.secret_key = '6hb4FGh7ja1sdd4'
    app.run(host='192.168.0.15',port=80, debug=True)
