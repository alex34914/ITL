from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Product, Order
from database import create_app

app = create_app()
CORS(app)

@app.route('/')
def index():
    return jsonify(message="Welcome to the Product and Order Management API!")

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data.get('name') or not data.get('price') or not data.get('stock'):
        return jsonify(message="Missing required fields: name, price, or stock"), 400
    try:
        product = Product(
            name=data['name'],
            category=data.get('category'),
            price=data['price'],
            stock=data['stock'],
            description=data.get('description')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(message="Product added successfully!"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Error adding product: {str(e)}"), 500

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    if not data.get('name') or not data.get('price') or not data.get('stock'):
        return jsonify(message="Missing required fields: name, price, or stock"), 400
    try:
        product.name = data['name']
        product.category = data['category']
        product.price = data['price']
        product.stock = data['stock']
        product.description = data.get('description')
        db.session.commit()
        return jsonify(message="Product updated successfully!")
    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Error updating product: {str(e)}"), 500

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify(message="Product deleted successfully!")
    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Error deleting product: {str(e)}"), 500

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(order.to_dict())

@app.route('/orders', methods=['POST'])
def add_order():
    data = request.get_json()
    if not data.get('product_id') or not data.get('quantity') or not data.get('total_amount'):
        return jsonify(message="Missing required fields: product_id, quantity, or total_amount"), 400
    try:
        order = Order(
            product_id=data['product_id'],
            quantity=data['quantity'],
            order_date=data['order_date'],
            total_amount=data['total_amount']
        )
        db.session.add(order)
        db.session.commit()
        return jsonify(message="Order added successfully!"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Error adding order: {str(e)}"), 500

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    data = request.get_json()
    order = Order.query.get_or_404(id)
    if not data.get('product_id') or not data.get('quantity') or not data.get('total_amount'):
        return jsonify(message="Missing required fields: product_id, quantity, or total_amount"), 400
    try:
        order.product_id = data['product_id']
        order.quantity = data['quantity']
        order.order_date = data['order_date']
        order.total_amount = data['total_amount']
        db.session.commit()
        return jsonify(message="Order updated successfully!")
    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Error updating order: {str(e)}"), 500

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    try:
        db.session.delete(order)
        db.session.commit()
        return jsonify(message="Order deleted successfully!")
    except Exception as e:
        db.session.rollback()
        return jsonify(message=f"Error deleting order: {str(e)}"), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)