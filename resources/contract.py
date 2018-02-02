from flask_restful import Resource, reqparse
from models.ContractModel import ContractModel
from scrap.scrap_emmap import EmmapScrap
from scrap.selenium_peaje  import Telepeaje_Scrap

class Contract(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('service',
                        type=int,
                        required=False,
                        help="This field cannot be blank.",
                        location=['values']
                       )
    parser.add_argument('usuario',
                        type=int,
                        required=False,
                        help="This field cannot be blank.",
                        location=['values']
                       )
    parser.add_argument('counterpart',
                        type=str,
                        required=False,
                        help="This field cannot be blank.",
                        location=['values']
                       )   

    def get(self, name):
        contract = ContractModel.find_by_id(name)
        if contract:
            return contract.json(), 200
        return {'message': 'Contract not found'}, 404

    def post(self):
        try:
            print('post contract')
            data = Contract.parser.parse_args()

            print('post contract 1')

            if ContractModel.find(data["service"], data["usuario"], data["counterpart"]):
                return {'message': "Un contrato con el servicio {servicio} con contrapartida {counterpart} ya existe.".format(
                    servicio=data["service"],
                    counterpart=data["counterpart"])}, 400

            contrato = ContractModel(**data)
            try:
                contrato.save_to_db()
            except:
                return {"message": "Un error ocurrio creando el contrato"}, 500

            return contrato.json(), 201
        except Exception as eg:
            return {"message": "Un error ocurrio general {error}".format(error=eg.args)}, 500

    def delete(self, name):
        store = ContractModel.find_by_id(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class ContractList(Resource):
    def get(self):
        return {'contract': [contract.json() for contract in ContractModel.query.all()]}


class ContractEnquiry(Resource):
    
    def get(self, id):
        
        contract = ContractModel.find_by_id(id)
                
        if contract.service.name == "agua":            
            scrapper = EmmapScrap(contract.service.url)
            result = scrapper.enquiry(contract.counterpart)            
            return {'contract ' : contract.id,
                    'resultado' : result}, 200
        elif contract.service.name == "telepeaje":
            scrapper = Telepeaje_Scrap(contract.service.url)
            result = scrapper.enquiry( contract.login, contract.password, contract.counterpart)
            return {'contract ': contract.id,
                    'resultado': result}, 200
            
