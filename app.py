from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

items = [
    {
        'name': 'lambo',
        'price': 500.0
    }
]


@app.route('/', methods=['GET'])
def home():
    return 'Hello, world!'


class Item(Resource):

    def get(self, name):
        item = next(filter(lambda _item: _item['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda _item: _item['name'] == name, items), None):
            return {'message': f'Item with name: {name} already exists'}, 400

        data = request.get_json()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201


class ItemList(Resource):

    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(port=5000, debug=True)
