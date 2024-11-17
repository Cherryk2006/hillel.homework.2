from functools import wraps

from flask import Flask, request, render_template, redirect, session
import sqlite3


app = Flask(__name__)

app.secret_key = 'abcd'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class DB_local(object):
    def __init__(self, file_name):
        self.con = sqlite3.connect(file_name)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.con.close()


def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        result = func(*args, **kwargs)
        return result
    return wrapped


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with DB_local(request.files['db3.db']) as db_project:
            db_project.execute('''SELECT * FROM user WHERE login = ? AND password = ?'''
                               , (username, password))
            user = db_project.fetchone()
            if user:
                session['user_id'] = user['login']
                return "Login Successful"
            else:
                return "Wrong Username or Password", 401

    if request.method == 'POST':
        return 'POST'


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        with DB_local('db3.db') as db_cur:
            form_data = request.form
            db_cur.execute('''INSERT INTO users
             (login, password, full_name, contacts, ipn, photo, passport) 
             VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (
                               form_data['login'], form_data['password'], form_data['full_name'],
                               form_data['contacts'], form_data['ipn'], form_data['photo'], form_data['passport']
                                       )
                           )
        return redirect('/login')


@app.route('/items', methods=['GET', 'POST'])
def items(db_project=None):
    if request.method == 'GET':
        with DB_local('db3.db') as db_cur:
            db_cur.execute("SELECT * FROM item")
            item = db_cur.fetchall()
        return render_template(items.html)
    if request.method == 'POST':
        with DB_local('db3.db') as db_cur:
            
            user_login = session['user_id']
            db_project.execute("SELECT id FROM user WHERE login = ?", (user_login,))
            user_id = db_project.fetchone()['id']
            
            query_args = request.form
            query_args['owner_id'] = user_id
            
            db_cur.execute('''INSERT INTO item (photo, name, description, price_hour, price_day, price_week, price_month, owner_id)
            VALUES (:photo, :name, :description, :price_hour, :price_day, :price_week, :price_month, :owner_id)''', query_args)
        return redirect("/item")


@app.route('/items/<int:item_id>', methods=['GET', 'DELETE'])
def item_detail(item_id):
    if request.method == 'GET':
        with DB_local('db3.db') as db_cur:
            db_cur.execute("SELECT * FROM item WHERE id = ?", (item_id,))
            item = db_cur.fetchone()
            return render_template(item.html)
        return f'GET {item_id}'
    if request.method == 'DELETE':
        with DB_local('db3.db') as db_cur:
            db_cur.execute("DELETE FROM item WHERE id = ?", (item_id,))
        return redirect('/items')


@app.route('/leasers', methods=['GET'])
def leasers():
    if request.method == 'GET':
        with DB_local('db3.db') as db_cur:
            db_cur.execute("SELECT * FROM leaser")
            leaser = db_cur.fetchall()
        return render_template("leasers.html")


@app.route('/leasers/<int:leaser_id>', methods=['GET'])
def leaser_detail(leaser_id):
    with DB_local('db3.db') as db_cur:
        db_cur.execute("SELECT * FROM leaser WHERE id = ?", (leaser_id,))
        leaser = db_cur.fetchone()
    if request.method == 'GET':
        return render_template("leasers.html")


@app.route('/contracts', methods=['GET', 'POST'])
@login_required
def contracts():
    if request.method == 'GET':
        with DB_local('db3.db') as db_cur:
            db_cur.execute("SELECT * FROM contract")
            contract = db_cur.fetchall()
        return render_template('contracts.html')

    if request.method == 'POST':
        query = """INSERT INTO contract (text, start_date, end_date, leaser, taker, item) VALUES (?, ?, ?, ?, ?, ?)"""

        with DB_local('db3.db') as db_project:
            db_project.execute("SELECT id FROM user WHERE login = ?", (session['user_id'],))
            my_id = db_project.fetchone()['id']
            taker_id = my_id
            item_id = request.form['item']
            leaser_id = request.form['leaser']
            db_project.execute("SELECT * FROM item WHERE id = ?", (item_id,))
            leaser = db_project.fetchone()['owner_id']

            contract_status = "pending"

            query_args = (request.form['text'], request.form['start_date'], request.form['end_date'], leaser, taker_id, item_id, contract_status)
            insert_query = """INSERT INTO contract (text, start_date, end_date, leaser, taker, item, status) VALUES (?, ?, ?, ?, ?, ?, ?)"""
            db_project.execute(insert_query, query_args)

        return 'POST'


@app.route('/contracts/<int:contract_id>', methods=['GET', 'PATCH', 'PUT'])
def contract_detail(contract_id):
    if request.method == 'GET':
        return f'GET {contract_id}'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'PUT':
        return 'PUT'


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'POST':
        return 'POST'


@app.route('/complain', methods=['POST'])
def complain():
    if request.method == 'POST':
        return 'POST'


@app.route('/compare', methods=['GET', 'PUT/PATCH'])
def compare():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'


@app.route('/profile', methods=['GET', 'PUT/PATCH', 'DELETE'])
def profile():
    if request.method == 'GET':
        with DB_local('db3.db') as db_cur:
            query = f'''SELECT full_name FROM user WHERE login = ?'''
            print(query)
            db_cur.execute(query, (session["user_id"],))
            full_name = db_cur.fetchone()['full_name']
        return render_template("user.html", full_name=full_name)
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'DELETE':
        return 'DELETE'


@app.route('/favorites', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def favorites():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'POST':
        return 'POST'
    if request.method == 'DELETE':
        return 'DELETE'
    if request.method == 'PATCH':
        return 'PATCH'


@app.route('/search_history', methods=['GET', 'DELETE'])
def search_history():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'DELETE':
        return 'DELETE'


if __name__ == '__main__':
    app.run()
