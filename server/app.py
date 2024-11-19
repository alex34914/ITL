from flask import Flask, request, jsonify
from database import create_app
from models import db, Product
from flask_cors import CORS
from typing import Union, Dict

app = create_app()
CORS(app)

@app.route('/products', methods=['GET'])
def get_products() -> Union[Dict[str, str], Dict[str, Union[str, int]]]:
    """
    Получает список всех продуктов из базы данных.
    
    :return: Список продуктов в формате JSON или сообщение об ошибке.
    """
    try:
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id: int) -> Union[Dict[str, str], Dict[str, Union[str, int]]]:
    """
    Получает продукт по его ID из базы данных.

    :param product_id: ID продукта.
    :return: Продукт в формате JSON или сообщение об ошибке.
    """
    try:
        product = Product.query.get(product_id)
        if product:
            return jsonify(product.to_dict()), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=['POST'])
def create_product() -> Union[Dict[str, str], Dict[str, Union[str, int]]]:
    """
    Создает новый продукт в базе данных.

    :return: Созданный продукт в формате JSON или сообщение об ошибке.
    """
    data = request.get_json()
    try:
        if not data.get('name') or data.get('price') is None or data.get('stock') is None:
            return jsonify({"error": "Fields 'name', 'price', and 'stock' are required"}), 400
        new_product = Product(
            name=data['name'],
            category=data.get('category'),
            price=float(data['price']),
            stock=int(data['stock']),
            description=data.get('description')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id: int) -> Union[Dict[str, str], Dict[str, Union[str, int]]]:
    """
    Обновляет информацию о продукте в базе данных.

    :param product_id: ID продукта.
    :return: Обновленный продукт в формате JSON или сообщение об ошибке.
    """
    data = request.get_json()
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        product.name = data.get('name', product.name)
        product.category = data.get('category', product.category)
        if 'price' in data:
            product.price = float(data['price'])
        if 'stock' in data:
            product.stock = int(data['stock'])
        product.description = data.get('description', product.description)
        db.session.commit()
        return jsonify(product.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id: int) -> Union[Dict[str, str], Dict[str, Union[str, int]]]:
    """
    Удаляет продукт из базы данных по его ID.

    :param product_id: ID продукта.
    :return: Сообщение об успешном удалении или ошибке.
    """
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
