from flask import Flask, jsonify, request, render_template

#### TO KILL A PROCESS ON A PORT
# ps -fA | grep python
# kill #### <--- Number for process grepped

app = Flask(__name__)

# @app.route('/') # 'http://wwww.google.com/'
# def home():
# 	return "Hello, world!"


# SERVER
# POST - used to receive data
# GET - used to send data back

# BROWSER
# POST - used to send data back
# GET - used to receive data


stores = [
	{
	'name': 'MyStore',
	'items': [
			{
			'name': 'Item1',
			'price': 15.99
			},
			{
			'name': 'Item2',
			'price': 1.99
			}
		]
	}
]


@app.route('/')
def home():
	return render_template('index.html')

# POST /store data: {name:}
# Create a store with a given name
@app.route('/store', methods=['POST'])
def create_store():
	request_data = request.get_json()
	new_store = {
		'name': request_data['name'],
		'items': []
	}
	stores.append(new_store)
	return jsonify(new_store)

# GET /store/<string:name>
# Get a store for a given name
@app.route('/store/<string:name>')
def get_store(name):
	# Iterate over stores
	for store in stores:
		# If the store name matches, return it
		if store['name'] == name:
			return jsonify(store)
	# If none match, return an error message
	return jsonify({'message': 'Store not found'})

# GET /store
# Return list of all stores
@app.route('/store')
def get_stores():
	return jsonify({'stores': stores}) # Becasue JSON can not be a list, and stores is a list. This turns the store list into a dictionary with 1 key

# POST /store/<string:name>/item {name:, prince:}
# Create an item within a store with a specific item name
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
	request_data = request.get_json()
	for store in stores:
		if store['name'] == name:
			new_item = {
				'name': request_data['name'],
				'price': request_data['price']
			}
			store['items'].append(new_item)
			return jsonify(new_item)
	return jsonify({'message': 'Store not found'})


# GET /store/<string:name>/item
# Get items within a specific store
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
	# Iterate over items in store
	for store in stores:
		# If the store name matches, return it
		if store['name'] == name:
			return jsonify({'items': store['items']})
	# If none match, return an error message
	return jsonify({'message': 'Store not found'})

app.run(port=5000)