import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be blank'
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {
                'item': {
                    'name': row[0],
                    'price': row[1]
                }
            }

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item, 200
        return {'message': f'Item with name: {name} not found'}, 400

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'message': f'Item with name: {name} already exists'}, 400
        data = self.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }

        self.insert(item)

        return item, 201

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        new_item = {
            'name': name,
            'price': data['price']
        }
        if self.find_by_name(name):
            self.update(new_item)
        else:
            self.insert(new_item)
        return new_item, 200

    @jwt_required()
    def delete(self, name):
        if not self.find_by_name(name):
            return {'message': f'Item with name: {name} not found'}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

        return {'message': f'Item with name: "{name}" is deleted'}, 200


class ItemList(Resource):

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        results = cursor.execute(query)
        items = [{'name': row[0], 'price': row[1]} for row in results]

        connection.close()
        return items, 200
