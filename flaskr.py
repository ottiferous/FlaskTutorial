import sqlite3
import ConfigParser
import duo_web as duo
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# config
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'dev key'
USERNAME = 'andrew'
PASSWORD = 'default'


# create flask application
app = Flask(__name__)
app.config.from_object(__name__)


# config parser
def grab_keys(filename='duo.conf'):
    config = ConfigParser.RawConfigParser()
    config.read(filename)

    akey = config.get('duo', 'akey')
    ikey = config.get('duo', 'ikey')
    skey = config.get('duo', 'skey')
    host = config.get('duo', 'host')
    return {'akey': akey, 'ikey': ikey, 'skey': skey, 'host': host}


# make a database connection
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# Request DB connections helpers
@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# Routing functions
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)', [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    result = grab_keys()
    sec = duo.sign_request(result['ikey'], result['skey'], result['akey'], "admin")
    if request.method == 'GET':
        return render_template('duoframe.html', duohost=result['host'], sig_request=sec)
    if request.method == 'POST':
        user = duo.verify_response(result['ikey'], result['skey'], result['akey'], request.args.get('sig_response'))
        if user:
            return render_template(url_for('mfa'), user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('mfa'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# main body
if __name__ == '__main__':
    app.run()
