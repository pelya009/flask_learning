from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from models.store import StoreModel


class Store(Resource):

    @jwt_required(optional=True)
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': f'Store with name: "{name}" not found'}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store with name: "{name}" already exists'}, 400
        store = StoreModel(name)
        store.save_to_db()

        return store.json(), 201

    @jwt_required(fresh=True)
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': f'Store with name: "{name}" is deleted'}, 200
        return {'message': f'Store with name: "{name}" not found'}, 404


class StoreList(Resource):

    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        stores = [store.json() for store in StoreModel.find_all()]
        if user_id:
            return stores, 200
        return [store['name'] for store in stores], 200
