from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from blacklist import BLACKLIST
from db import db
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'foobar'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()
    user = UserModel(username='admin', password='admin')
    user.save_to_db()
    store = StoreModel(name='italian_auto')
    store.save_to_db()
    item = ItemModel(name='lambo', price=500.0, store_id=1)
    item.save_to_db()


jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    return 'Token is expired', 401


@jwt.invalid_token_loader
def invalid_token_callback(err):
    return f'Provided Bearer is not a valid JWT token: {err}', 401


@jwt.unauthorized_loader
def unauthorized_token_callback(err):
    return f'Bearer token is not provided: {err}', 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_headers, jwt_payload):
    return 'The token is no longer valid. You need the fresh one.', 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_headers, jwt_payload):
    return 'The token is revoked', 401


@app.route('/', methods=['GET'])
def home():
    return 'Hello, world!'


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
