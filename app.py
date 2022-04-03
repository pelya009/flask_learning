from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from datetime import timedelta

from db import db
from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobar'
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


app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)


@app.route('/', methods=['GET'])
def home():
    return 'Hello, world!'


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
