import sqlite3
from functools import wraps

import db
from flask import Flask, request, render_template, redirect, session, jsonify
from sqlalchemy import select
from sqlalchemy.sql.functions import current_user

import models
from database import init_db, db_session

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


class DbHandle:
    db_filter = 'db3.db'

    def select(self, table_name, filter_dict=None, join_table=None, join_conditions=None):
        if filter_dict is None:
            filter_dict = {}
        with DB_local(self.db_filter) as db_cur:
            query = f'SELECT * FROM {table_name}'

            if join_table is not None:
                query += f' JOIN {join_table} as right_table ON '
                join_conditions_list = []
                for left_field, right_field in join_conditions:
                    join_conditions_list.append(f'{table_name}.{left_field} = right_table.{right_field}')
                query += ' AND '.join(join_conditions_list)

            if filter_dict:
                query += ' WHERE '
                itms = []
                for key, value in filter_dict.items():
                    itms.append(f'{key} = ?')
                query += ' AND '.join(itms)

            db_cur.execute(query, tuple(value for key, value in filter_dict.items()))
            return db_cur.fetchall()

    def insert(self, table_name, data_dict):
        with DB_local(self.db_filter) as db_cur:
            query = f'INSERT INTO {table_name}('
            query += ','.join(data_dict.keys())
            query += ') VALUES ('
            query += ','.join([f':{itm}' for itm in data_dict.keys()])
            query += ')'
            # insert into {table_name} (a1, a2, a3) values (:?, :?, :?)
            db_cur.execute(query, data_dict)


db_connector = DbHandle()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        init_db()
        query = select(models.User).where(username == models.User.login)
        user_data = db.session.execute(query).first()

        if user_data:
            session['user_id'] = user_data[0]['login']
            return "Login Successful"
        else:
            return "Wrong Username or Password", 401


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        form_data = dict(request.form)
        init_db()
        user = models.User(**form_data)
        db_session.add(user)
        db_session.commit()
        db_connector.insert('user', form_data)
        return redirect('/login')


@app.route('/items', methods=['GET', 'POST'])
def items(db_project=None, items=None):
    if request.method == 'GET':
        init_db()
        items_query = select(models.Item)
        items = list(db.session.execute(items).scalars())
        return render_template('items.html', items=items)

    if request.method == 'POST':
        if session.get('user_id') is None:
            return redirect('/login')
        else:
            init_db()
            user_id = db_connector.select('user', {'login': session['user_id']})[0]['login']
            current_user = db_connector.scalar(select(models.User).where(models.User.login == session['logged_in']))
            
            query_args = dict(request.form)
            query_args['owner_id'] = current_user.id
            new_item = models.Item(**query_args)

            db_session.add(new_item)
            db_session.commit()
            return redirect("/item")


@app.route('/items/<int:item_id>', methods=['GET', 'DELETE'])
def item_detail(item_id):
    item = db_session.query(models.Item).get(item_id)
    if request.method == 'GET':
        return jsonify({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price_hour': item.price_hour,
            'price_day': item.price_day,
            'price_week': item.price_week,
            'price_month': item.price_month
        }) if item else ("Item not found", 404)
    elif request.method == 'DELETE':
        if 'user_id' not in session or item.owner_id != session['user_id']:
            return "Unauthorized", 403
        db_session.delete(item)
        db_session.commit()
        return redirect('/items')

@app.route('/leasers', methods=['GET'])
def leasers():
    if request.method == 'GET':
        leasers = db_connector.select('leasers')
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
        contracts = db_connector.select('contracts')
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

            query_args = (request.form['text'], request.form['start_date'], request.form['end_date'], leaser, taker_id,
                          item_id, contract_status)
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
