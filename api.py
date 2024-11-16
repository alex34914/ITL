from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from models import db, Product, Order
from database import create_app

app = create_app()
CORS(app)

# Настройка API и документации Swagger
api = Api(app, version='1.0', title='Product and Order API',
          description='An API to manage products and orders')

# Создание пространства имен для продуктов и заказов
product_ns = api.namespace('products', description='Operations related to products')
order_ns = api.namespace('orders', description='Operations related to orders')

# Модели для валидации данных через Swagger
product_model = api.model('Product', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a product'),
    'name': fields.String(required=True, description='The name of the product'),
    'category': fields.String(required=True, description='The category of the product'),
    'price': fields.Float(required=True, description='The price of the product'),
    'stock': fields.Integer(required=True, description='The stock quantity of the product'),
    'description': fields.String(description='The description of the product')
})

order_model = api.model('Order', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an order'),
    'product_id': fields.Integer(required=True, description='The product identifier'),
    'quantity': fields.Integer(required=True, description='The quantity of the product ordered'),
    'order_date': fields.String(required=True, description='The date of the order'),
    'total_amount': fields.Float(required=True, description='The total amount of the order')
})

# Роуты для продуктов
@product_ns.route('/')
class ProductList(Resource):
    @product_ns.doc('get_products')
    def get(self):
        """Получить список всех продуктов"""
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])

    @product_ns.doc('create_product')
    @product_ns.expect(product_model)
    def post(self):
        """Добавить новый продукт"""
        data = request.get_json()
        product = Product(
            name=data['name'],
            category=data['category'],
            price=data['price'],
            stock=data['stock'],
            description=data.get('description')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify(message="Product added successfully!"), 201


@product_ns.route('/<int:id>')
@product_ns.response(404, 'Product not found')
@product_ns.param('id', 'The product identifier')
class ProductResource(Resource):
    @product_ns.doc('get_product')
    def get(self, id):
        """Получить продукт по ID"""
        product = Product.query.get_or_404(id)
        return jsonify(product.to_dict())

    @product_ns.doc('update_product')
    @product_ns.expect(product_model)
    def put(self, id):
        """Обновить продукт по ID"""
        data = request.get_json()
        product = Product.query.get_or_404(id)
        product.name = data['name']
        product.category = data['category']
        product.price = data['price']
        product.stock = data['stock']
        product.description = data.get('description')
        db.session.commit()
        return jsonify(message="Product updated successfully!")

    @product_ns.doc('delete_product')
    def delete(self, id):
        """Удалить продукт по ID"""
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify(message="Product deleted successfully!")

# Роуты для заказов
@order_ns.route('/')
class OrderList(Resource):
    @order_ns.doc('get_orders')
    def get(self):
        """Получить список всех заказов"""
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders])

    @order_ns.doc('create_order')
    @order_ns.expect(order_model)
    def post(self):
        """Добавить новый заказ"""
        data = request.get_json()
        order = Order(
            product_id=data['product_id'],
            quantity=data['quantity'],
            order_date=data['order_date'],
            total_amount=data['total_amount']
        )
        db.session.add(order)
        db.session.commit()
        return jsonify(message="Order added successfully!"), 201


@order_ns.route('/<int:id>')
@order_ns.response(404, 'Order not found')
@order_ns.param('id', 'The order identifier')
class OrderResource(Resource):
    @order_ns.doc('get_order')
    def get(self, id):
        """Получить заказ по ID"""
        order = Order.query.get_or_404(id)
        return jsonify(order.to_dict())

    @order_ns.doc('update_order')
    @order_ns.expect(order_model)
    def put(self, id):
        """Обновить заказ по ID"""
        data = request.get_json()
        order = Order.query.get_or_404(id)
        order.product_id = data['product_id']
        order.quantity = data['quantity']
        order.order_date = data['order_date']
        order.total_amount = data['total_amount']
        db.session.commit()
        return jsonify(message="Order updated successfully!")

    @order_ns.doc('delete_order')
    def delete(self, id):
        """Удалить заказ по ID"""
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return jsonify(message="Order deleted successfully!")

if __name__ == '__main__':
    app.run(port=5001, debug=True)
