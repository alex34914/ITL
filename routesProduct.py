from flask import jsonify, request
from flask_restx import Namespace, Resource
from models import db, Product
from modelsApi import create_models

product_ns = Namespace('products', description='Operations related to products')
api = product_ns

product_model, _ = create_models(api)

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
