import psycopg2
from flask_restful import Resource, reqparse
from models.UserModel import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location=['values']
                       )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location=['values']
                       )
    parser.add_argument('mail',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location=['values']
                       )
    parser.add_argument('mobile',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location=['values']
                       )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserList(Resource):
    def get(self):
        print('get user list')
        return {'user': [user.json() for user in UserModel.query.all()]}, 200
