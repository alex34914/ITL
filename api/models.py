from flask_restx import fields, Api


def create_models(api: Api):
    """
    Создает модели для продуктов и заказов с помощью flask_restx.
    :param api: Экземпляр Api, используемый для создания моделей
    :return: Кортеж, содержащий модели Product и Order
    """
    product_model = api.model('Product', {
        'id': fields.Integer(readOnly=True, description='The unique identifier of a product'),
        'name': fields.String(required=True, description='The name of the product', example='Laptop'),
        'category': fields.String(required=True, description='The category of the product', example='Electronics'),
        'price': fields.Float(required=True, description='The price of the product', example=1299.99),
        'stock': fields.Integer(required=True, description='The stock quantity of the product', example=100),
        'description': fields.String(description='The description of the product', example='High-performance laptop')
    })
    order_model = api.model('Order', {
        'id': fields.Integer(readOnly=True, description='The unique identifier of an order'),
        'product_id': fields.Integer(required=True, description='The product identifier', example=1),
        'quantity': fields.Integer(required=True, description='The quantity of the product ordered', example=2),
        'order_date': fields.String(required=True, description='The date of the order', example='2024-11-16'),
        'total_amount': fields.Float(required=True, description='The total amount of the order', example=2599.98)
    })
    return product_model, order_model
