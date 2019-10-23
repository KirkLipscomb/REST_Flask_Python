from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from resources.user import UserRegister
from models.store_model import StoreModel


class Store(Resource):

    # @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            status = 200
            result = store.json()
        else:
            status = 404
            result = {'message': f'Store not found: {name}'}

        return result, status

    def post(self, name):
        if StoreModel.find_by_name(name):
            # We already have this item
            result = {'message': f'A store with name {name} already exists.'}
            status = 400
        else:
            store = StoreModel(name,)
            try:
                store.save_to_database()
                status = 201
                result = store.json()
            except:
                result = {'message': f'Internal Error Inserting Store: {name}'}
                status = 500

        return result, status

    def delete(self, name):
        try:
            store = StoreModel.find_by_name(name)
            if store:
                store.delete()
                result = {'message': f'Store deleted: {name}'}
                status = 200
            else:
                result = {'message': f'Store not found: {name}'}
                status = 404
        except:
            result = {'message': f'Internal Error Deleting Store: {name}'}
            status = 500

        return result, status


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
