from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
                'name': 'My Item',
                'price': 15.99
            }
        ]
    }
]

# POST to receive data
# GET to send data   (server's perspective)

# POST /store   data: {name:}
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
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores
    # If the store name matches, return it
    # If non match, return an error message
    match = jsonify({'message': f'ERROR: Store named "{name}" not found'})
    for store in stores:
        if store['name'] == name:
            match = jsonify(store)
    return match


# GET /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    new_item = {
        'name': request_data['name'],
        'price': request_data['price']
    }

    result = jsonify({'message', f'ERROR: Store named "{name}" not found'})
    for store in stores:
        if store['name'] == name:
            store['items'].append(new_item)
            result = jsonify(new_item)
    return result


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    match = jsonfiy({'message': f'ERROR: Store named "{name}" not found'})
    for store in stores:
        if store['name'] == name:
            match = jsonify({'items': store['items']})
    return match


app.run(port=5000)
