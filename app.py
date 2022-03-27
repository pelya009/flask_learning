from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'roman',
        'items': [
            {
                'name': 'lambo',
                'price': 500.0
            }
        ]
    }
]


@app.route('/', methods=['GET'])
def home():
    return 'Hello, world!'


@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store), 201


@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store), 200
    return jsonify('Store not found'), 404


@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify([store['name'] for store in stores])


@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    for store in stores:
        if store['name'] == name:
            request_data = request.get_json()
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item), 201
    return jsonify('Store not found'), 404


@app.route('/store/<string:name>/item', methods=['GET'])
def get_items(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']}), 200
    return jsonify('Store not found'), 404


app.run(port=5000)
