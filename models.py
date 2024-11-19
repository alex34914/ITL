# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    """
    Модель для представления продукта.
    """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name: str, category: str, price: float, stock: int, description: str = None):
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description

    def __repr__(self) -> str:
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "description": self.description
        }

class Order(db.Model):
    """
    Модель для представления заказа.
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.String(10), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))

    def __init__(self, product_id: int, quantity: int, order_date: str, total_amount: float):
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date
        self.total_amount = total_amount

    def __repr__(self) -> str:
        return f'<Order {self.id} - Product {self.product_id}>'
