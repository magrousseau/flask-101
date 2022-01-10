# wsgi.py
# pylint: disable=missing-docstring

from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = {
    1: { 'id': 1, 'name': 'Skello' },
    2: { 'id': 2, 'name': 'Socialive.tv' },
    3: { 'id': 3, 'name': 'Le Wagon'},
}

@app.route('/')
def hello():
    return "Hello my World!"

@app.route('/api/v1/products')
def products():
    products = list(PRODUCTS.values())
    return jsonify(products)
