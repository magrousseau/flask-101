# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, jsonify, abort, request

app = Flask(__name__)

PRODUCTS = {
    1: {'id': 1, 'name': 'Skello'},
    2: {'id': 2, 'name': 'Socialive.tv'},
    3: {'id': 3, 'name': 'Le Wagon'},
}


@app.route('/')
def hello():
    return "Hello my World!"


@app.route('/api/v1/products')
def read_many_products():
    products = list(PRODUCTS.values())
    return jsonify(products), 200


@app.route('/api/v1/products/<int:product_id>', methods=['GET'])
def read_one_product(product_id):
    product = PRODUCTS.get(product_id)
    if product is None:
        abort(404)
    return jsonify(product), 200


@app.route('/api/v1/products/<int:product_id>', methods=['DELETE'])
def delete_one_product(product_id):
    product = PRODUCTS.get(product_id)
    if product is None:
        abort(404)
    else:
        del PRODUCTS[product_id]
    return '', 204
    # product = PRODUCTS.pop(product_id, None)

    # if product is None:
    #     abort(404)  # No product of product_id found is a Not Found Error
    # return '', 204


@app.route('/api/v1/products', methods=['POST'])
def create_one_product():
    data = request.get_json()
    if data is None:
        abort(400)  # Missing needed field(s) is a Bad Request Error

    name = data.get('name')

    if name is None:
        abort(400)  # Missing needed field is a Bad Request Error

    if name == '' or not isinstance(name, str):
        abort(422)  # Bad format for needed field is a Unprocessable Entity Error

    next_id = max(PRODUCTS.keys()) + 1
    PRODUCTS[next_id] = {'id': next_id, 'name': name}

    # We need to return the entire entity to comunicate the new id to the api consumer
    # This way, he can act on this resource using his id.
    #
    # We could simply return the id, but it's not in the REST spirit
    # => Don't forget : /<entity>/<entity_id> represents an entire entity
    return jsonify(PRODUCTS[next_id]), 201  # Created


@app.route('/api/v1/products/<int:product_id>', methods=['PATCH'])
def update_one_product(product_id):
    data = request.get_json()
    if data is None:
        abort(400)

    name = data.get('name')

    if name is None:
        abort(400)

    if name == '' or not isinstance(name, str):
        abort(422)

    product = PRODUCTS.get(product_id)

    if product is None:
        abort(404)

    PRODUCTS[product_id]['name'] = name

    # Update action (UPDATE method) no need to return the entity since we know what we modified
    return '', 204
