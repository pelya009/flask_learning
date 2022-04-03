from flask_jwt import jwt_required
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': f'Store with name: "{name}" not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store with name: "{name}" already exists'}, 400
        store = StoreModel(name)
        store.save_to_db()

        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': f'Store with name: "{name}" is deleted'}, 200
        return {'message': f'Store with name: "{name}" not found'}, 404


class StoreList(Resource):

    def get(self):
        return [store.json() for store in StoreModel.query.all()]
