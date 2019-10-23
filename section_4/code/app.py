from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'Chalet'
api = Api(app)

# jwt will create a new endpoint of /auth which accepts username and password
# /auth returns a JWT token
# Uses token to authenticate
jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be empty')

    @jwt_required()
    def get(self, name):
        item = next(
            filter(lambda x: (x['name'] == name), items), None)
        return item, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: (x['name'] == name), items), None):
            # We already have this item
            item = {'message': f'An item with name {name} already exists.'}
            status = 400
        else:
            data = Item.parser.parse_args()
            item = {'name': name, "price": data['price']}
            items.append(item)
            status = 201
        return item, status

    def delete(self, name):
        item = next(filter(lambda x: (x['name'] == name), items), None)
        if item:
            items.remove(item)
        return item, 200 if item else 404

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: (x['name'] == name), items), None)
        if item:
            item.update(data)
            status = 200
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
            status = 201
        return item, status


class ItemList(Resource):
    def get(self):
        return items, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000)
