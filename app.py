from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

#from security import authenticate, identity
from resources.user import UserRegister, UserList
from resources.service import Service, ServiceList
from resources.contract import Contract, ContractList, ContractEnquiry

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kratos:12345@localhost/pbot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'franco'
api = Api(app)

#jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Service, '/service/<string:name>')
api.add_resource(ServiceList, '/services')

api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')

api.add_resource(Contract, '/contract')
api.add_resource(ContractEnquiry, '/contract/<int:id>/enquiry')
api.add_resource(ContractList, '/contracts')


if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            print('creando tablas on request ')
            db.create_all()

    app.run(port=5002)
