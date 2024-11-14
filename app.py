import sqlite3

from flask import Flask, request, render_template, redirect

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


app = Flask(__name__)

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
                return "Login Successful"
            else:
                return "Incorect Username or Password", 401

    if request.method == 'POST':
        return 'POST'

@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'POST':
        return 'POST'
    if request.method == 'DELETE':
        return 'DELETE'

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
def items():
    if request.method == 'GET':
        with DB_local('db3.db') as db_cur:
            db_cur.execute("SELECT * FROM item")
            items = db_cur.fetchall()
        return render_template(items.html)
    if request.method == 'POST':
        with DB_local('db3.db') as db_cur:
            db_cur.execute('''INSERT INTO items (photo, name, description, price_hour, price_day, price_week, price_month)
            VALUES (:photo, :name, :description, :price_hour, :price_day, :price_week, :price_month)''', request.form)
        return redirect('/items')

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
            db_cur.execute("SELECT * FROM leasers")
            leasers = db_cur.fetchall()
        return render_template("leasers.html")

@app.route('/leasers/<int:leaser_id>', methods=['GET'])
def leaser_detail(leaser_id):
    with DB_local('db3.db') as db_cur:
        db_cur.execute("SELECT * FROM leaser WHERE id = ?", (leaser_id,))
        leaser = db_cur.fetchone()
    if request.method == 'GET':
        return render_template("leasers.html")

@app.route('/contracts', methods=['GET', 'POST'])
def contracts():
    if request.method == 'GET':
        with DB_local('db3.db') as db_cur:
            db_cur.execute("SELECT * FROM contracts")
            contracts = db_cur.fetchall()
        return render_template('contracts.html')

    if request.method == 'POST':
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
        return render_template("user.html")
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
'''
/profile (/user, /me) [GET, PUT(PATCH), DELETE]
      ?  /favouties [GET, POST, DELETE, PATCH]
      ??  /favouties/<favourite_id> [DELETE]
      ?  /search_history [GET, DELETE]
'''