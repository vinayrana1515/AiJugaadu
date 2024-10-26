from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from db import db  # Import the db instance from db.py
from models import User, Product, Order, Cart, Purchase, Session, Message

app = Flask(__name__)
CORS(app)

# PostgreSQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Helloworld%40123@localhost:5432/aiJugaadu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Route to fetch all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

# Route to add a product to the cart
@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    cart_item = Cart(
        product_id=data['product_id'],
        user_id=data['user_id'],
        final_price=data['final_price']
    )
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Product added to cart successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)

