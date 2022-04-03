from flask_jwt_extended import jwt_required, get_jwt_identity
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
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item needs a store id'
    )

    @jwt_required(optional=True)
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': f'Item with name: "{name}" not found'}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'Item with name: "{name}" already exists'}, 400
        data = self.parser.parse_args()

        item = ItemModel(name, **data)
        item.save_to_db()

        return item.json(), 201

    @jwt_required(fresh=True)
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()
        return item.json(), 200

    @jwt_required(fresh=True)
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'Item with name: "{name}" is deleted'}, 200
        return {'message': f'Item with name: "{name}" not found'}, 404


class ItemList(Resource):

    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return items, 200
        return [item['name'] for item in items], 200
