from flask_restx import fields
from flask_restx import Api

def create_models(api: Api):
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

    return product_model, order_model