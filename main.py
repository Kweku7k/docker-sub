import pprint

import requests
from flask import Flask, jsonify, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)  #We want the same id as the django application
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

    def __to_dict__(self):
        return {
            "id": self.id,
            "title": self.title,
            "image": self.image
        }


class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/')
def index():
    return 'Hello'


@app.route('/api/products')
def get_products():
    products = Product.query.all()
    # return jsonify(products)
    return jsonify([product.__to_dict__() for product in products])


@app.route('/api/products/<int:id>/like')
def like(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()
    pprint.pprint(json)

    try:
        productUser = ProductUser(user_id=json['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()

        publish('product_liked', id)

    #     event
    except Exception as e:
        print(e)
        print("error")
        abort(400, 'You already liked this product')

    return jsonify({
        "message":"success"
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
