from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json(), 200

		return {'message': 'Store with name {} not found'.format(name)}, 404

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': 'Store with name {} already exists'.format(name)}, 400

		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'message': 'An error occurred whil creating the store.'}, 500

		return store.json(), 201

	def delete(swlf, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
		else:
			return {'message': 'Store with name {} does not exist.'}, 404

		return {'message': 'Store deleted'}

class StoreList(Resource):
	def get(self):
		return {'stores': [i.json() for i in StoreModel.query.all()]}