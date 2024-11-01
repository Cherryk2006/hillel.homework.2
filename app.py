from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'GET'
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
        return 'GET'
    if request.method == 'POST':
        return 'POST'

@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'POST':
        return 'POST'

@app.route('/items/<int:item_id>', methods=['GET', 'DELETE'])
def item_detail(item_id):
    if request.method == 'GET':
        return f'GET {item_id}'
    if request.method == 'DELETE':
        return f'DELETE {item_id}'

@app.route('/leasers', methods=['GET'])
def leasers():
    return 'GET'

@app.route('/leasers/<int:leaser_id>', methods=['GET'])
def leaser_detail(leaser_id):
    if request.method == 'GET':
        return f'GET {leaser_id}'

@app.route('/contracts', methods=['GET', 'POST'])
def contracts():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'POST':
        return 'POST'

@app.route('/contracts/<int:contract_id>', methods=['GET', 'PATCH/PUT'])
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
        return 'GET'
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