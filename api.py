from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from database import create_app
from routesProduct import product_ns
from routesOrder import order_ns

app = create_app()
CORS(app)

api = Api(app, version='1.0', title='Product and Order API',
          description='An API to manage products and orders')

# Регистрация пространств имен (namespaces)
api.add_namespace(product_ns)
api.add_namespace(order_ns)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
