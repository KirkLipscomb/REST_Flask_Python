import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='username is Required')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='password is Required')

    def post(self):
        data = UserRegister.parser.parse_args()
        user = UserModel.find_by_username(data['username'])

        if user:
            message = 'User already exists'
            status = 400
        else:
            user = UserModel(data['username'], data['password'])
            user.save_to_database()
            message = 'User created successfully'
            status = 201

        return {'message': message}, status
