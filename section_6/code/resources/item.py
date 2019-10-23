import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from resources.user import UserRegister
from models.item_model import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be empty')

    # @jwt_required()

    def get(self, name):
        item = ItemModel.get_item(name)
        if item:
            status = 200
            result = item.json()
        else:
            result = {'message': f'Item not found: {name}'}
            status = 404
        return result, status

    def post(self, name):
        if ItemModel.get_item(name):
            # We already have this item
            result = {'message': f'An item with name {name} already exists.'}
            status = 400
        else:
            data = Item.parser.parse_args()
            item = ItemModel(name, data['price'])
            try:
                item.add_item()
                status = 201
                result = item.json()
            except:
                result = {'message': f'Internal Error Inserting Item: {name}'}
                status = 500

        return result, status

    def delete(self, name):
        try:
            item = ItemModel.get_item(name)
            if item:
                item.delete()
                result = {'message': f'Item deleted: {name}'}
                status = 200
            else:
                result = {'message': f'Item not found: {name}'}
                status = 404
        except:
            result = {'message': f'Internal Error Deleting Item: {name}'}
            status = 500

        return result, status

    def put(self, name):
        try:
            data = Item.parser.parse_args()
            item = ItemModel.get_item(name)
            if item:
                # Item exists. Update it.
                item.price = data['price']
                item.update()
                status = 200
            else:
                item = ItemModel(name, data['price'])
                item.add_item()
                status = 201
            result = item.json()
        except:
            result = {'message': f'Internal Error Putting Item: {name}'}
            status = 500

        return result, status


class ItemList(Resource):
    def get(self):
        try:
            items = ItemModel.get_all_items()
            items_json = []
            for item in items:
                items_json.append(item.json())
            result = {'items': items_json}
            status = 200
        except:
            result = {'message': 'Internal Error Getting Items List'}
            status = 500

        return result, status
