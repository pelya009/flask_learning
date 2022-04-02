from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be blank'
    )

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': f'Item with name: {name} not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Item with name: {name} already exists'}, 400
        data = self.parser.parse_args()

        item = ItemModel(name, data['price'])
        item.save_to_db()

        return item.json(), 201

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])

        item.save_to_db()
        return item.json(), 200

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'Item with name: "{name}" is deleted'}, 200
        return {'message': f'Item with name: {name} not found'}, 404


class ItemList(Resource):

    def get(self):
        return [item.json() for item in ItemModel.query.all()], 200
