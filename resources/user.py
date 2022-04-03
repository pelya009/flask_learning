import hmac

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt,
    get_jwt_identity,
)
from flask_restful import Resource, reqparse

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help='This field cannot be blank'
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help='This field cannot be blank'
)


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return f"User with name: {data['username']} already exists", 400

        user = UserModel(**data)
        user.save_to_db()

        return {'id': user.id}, 201


class User(Resource):

    @classmethod
    @jwt_required(fresh=True)
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json(), 200
        return 'User not found', 404

    @classmethod
    @jwt_required(fresh=True)
    def delete(cls, user_id):
        claims = get_jwt()
        if not claims['is_admin']:
            return 'You need admin permissions', 403
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return 'User is deleted', 200
        return 'User not found', 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and hmac.compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return 'Invalid credentials', 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message': 'Logged out successfully'}, 200


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        return {'access_token': new_token}, 200
