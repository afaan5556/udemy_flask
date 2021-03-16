from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = 'Bummiesjelly310'

jwt = JWT(app, authenticate, identity) # creates /auth endpoint

items = []

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price',
		type=float,
		required=True,
		help='This field can not be blank!'
	)

	@jwt_required()
	def get(self, name):
		item = next(filter(lambda x: x['name'] == name, items), None)
		return {'item': item}, 200 if item else 404 # 200 is success and 404 is invalid

	def post(self, name):
		if next(filter(lambda x: x['name'] == name, items), None) is not None:
			return {'message': 'An item with name {} already exists'.format(name)}, 400 # 400 is bad request

		data = Item.parser.parse_args()

		item = {'name': name, 'price': data['price']}
		items.append(item)
		return item, 201

	def delete(self, name):
		global items
		if next(filter(lambda x: x['name'] == name, items), None) is None:
			return {'message': 'Item does not exist'}

		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item deleted'}

	def put(self, name):
		data = Item.parser.parse_args()

		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data)
		return item

class ItemList(Resource):
	def get(self):
		return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)