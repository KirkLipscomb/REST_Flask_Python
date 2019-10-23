from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Train\\REST_Flask_Python\\data\\data.db'
app.secret_key = 'Chalet'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# jwt will create a new endpoint of /auth which accepts username and password
# /auth returns a JWT token
# Uses token to authenticate
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    # Prevents running app if called becaus app.py is imported
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
