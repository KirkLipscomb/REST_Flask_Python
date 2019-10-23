import sqlite3
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserRegister


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be empty')

    @classmethod
    def get_item(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT name, price FROM items WHERE name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            item = {'item': {'name': row[0], 'price': row[1]}}
        else:
            item = None

        return item

    @classmethod
    def add_item(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (item['name'], item['price'],))
        connection.commit()
        connection.close()

    # @jwt_required()

    def get(self, name):
        item = self.get_item(name)
        if item:
            status = 200
        else:
            item = {'message': f'Item not found: {name}'}
            status = 404
        return item, status

    def post(self, name):
        if self.get_item(name):
            # We already have this item
            item = {'message': f'An item with name {name} already exists.'}
            status = 400
        else:
            data = Item.parser.parse_args()
            item = {'name': name, "price": data['price']}
            try:
                self.add_item(item)
                status = 201
            except:
                item = {'message': f'Internal Error Inserting Item: {name}'}
                status = 500

        return item, status

    def delete(self, name):
        if self.get_item(name):
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'DELETE FROM items WHERE name = ?'
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            item = {'message': f'Item deleted: {name}'}
            status = 200
        else:
            item = {'message': f'Item not found: {name}'}
            status = 404

        return item, status

    def put(self, name):
        data = Item.parser.parse_args()
        item = self.get_item(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = 'UPDATE items SET price = ? WHERE name = ?'
            try:
                cursor.execute(query, (data['price'], name,))
                connection.commit()
                connection.close()
                status = 200
            except:
                item = {'message': f'Internal Error Updating Item: {name}'}
                status = 500
        else:
            item = {'name': name, 'price': data['price']}
            try:
                self.add_item(item)
                status = 201
            except:
                item = {'message': f'Internal Error Inserting Item: {name}'}
                status = 500

        return item, status


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT name, price FROM items ORDER BY name'
        result = cursor.execute(query)
        rows = result.fetchall()
        connection.close()

        items = []
        for row in rows:
            items.append({'name': row[0], 'price': row[1]})

        return {'items': items}, 200
