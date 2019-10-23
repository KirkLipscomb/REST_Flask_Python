import sqlite3
from flask_restful import Resource, reqparse


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
        if User.find_by_username(data['username']):
            message = 'User already exists'
            status = 400
        else:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = 'INSERT INTO users VALUES (NULL, ?, ?)'
            cursor.execute(query, (data['username'], data['password']))

            connection.commit()
            connection.close()

            message = 'User created successfully'
            status = 201

        return {'message': message}, status
