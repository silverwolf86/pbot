from flask_restful import Resource, reqparse
from models.ServiceModel import ServiceModel


class Service(Resource):
    def get(self, name):
        store = ServiceModel.find_by_name(name)
        if store:
            return store.json(), 200
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if ServiceModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = ServiceModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = ServiceModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class ServiceList(Resource):
    def get(self):
        print('get list')
        return {'service': [store.json() for store in ServiceModel.query.all()]}, 200
