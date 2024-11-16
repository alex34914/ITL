from flask import jsonify, request
from flask_restx import Namespace, Resource
from models import db, Product
from api.models import create_models


product_ns = Namespace('products', description='Operations related to products')
api = product_ns
product_model, _ = create_models(api)


@product_ns.route('/')
class ProductList(Resource):
    """
    Класс для обработки запросов, связанных со списком продуктов.
    """
    @product_ns.doc('get_products')
    def get(self):
        """
        Получить список всех продуктов.
        :return: Список всех продуктов в формате JSON.
        """
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products])

    @product_ns.doc('create_product')
    @product_ns.expect(product_model)
    def post(self):
        """
        Добавить новый продукт.
        :return: Сообщение об успешном добавлении продукта в формате JSON.
        """
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
    """
    Класс для обработки запросов, связанных с конкретным продуктом.
    """
    @product_ns.doc('get_product')
    def get(self, id: int):
        """
        Получить продукт по его идентификатору (ID).
        :param id: Идентификатор продукта.
        :return: Продукт в формате JSON.
        """
        product = Product.query.get_or_404(id)
        return jsonify(product.to_dict())

    @product_ns.doc('update_product')
    @product_ns.expect(product_model)
    def put(self, id: int):
        """
        Обновить данные продукта по его идентификатору (ID).
        :param id: Идентификатор продукта.
        :return: Сообщение об успешном обновлении продукта в формате JSON.
        """
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
    def delete(self, id: int):
        """
        Удалить продукт по его идентификатору (ID).
        :param id: Идентификатор продукта.
        :return: Сообщение об успешном удалении продукта в формате JSON.
        """
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        return jsonify(message="Product deleted successfully!")
