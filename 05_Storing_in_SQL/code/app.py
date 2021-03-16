from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
api = Api(app)
app.secret_key = 'Bummiesjelly310'

jwt = JWT(app, authenticate, identity) # creates /auth endpoint

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__': # Make sure app is run when file is run but not if file is imported
	app.run(port=5000, debug=True)