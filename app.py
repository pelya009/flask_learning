from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from datetime import timedelta

from db import db
from resources.item import Item, ItemList
from resources.user import UserRegister
from security import authenticate, identity


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobar'
api = Api(app)

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
jwt = JWT(app, authenticate, identity)


@app.route('/', methods=['GET'])
def home():
    return 'Hello, world!'


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
