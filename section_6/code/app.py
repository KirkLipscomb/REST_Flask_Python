from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'Chalet'
api = Api(app)

# jwt will create a new endpoint of /auth which accepts username and password
# /auth returns a JWT token
# Uses token to authenticate
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # Prevents running app if called becaus app.py is imported
    app.run(port=5000, debug=False)
