from flask import jsonify, request
from flask_restx import Namespace, Resource
from models import db, Order
from modelsApi import create_models

order_ns = Namespace('orders', description='Operations related to orders')
api = order_ns

_, order_model = create_models(api)

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
