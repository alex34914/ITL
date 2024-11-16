from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __init__(self, name, category, price, stock, description=None):
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description

    def __repr__(self):
        return f'<Product {self.name}>'

    def price_category(self):
        """Метод для категоризации цены продукта."""
        if self.price < 1000:
            return 'Low'
        elif 1000 <= self.price <= 10000:
            return 'Medium'
        else:
            return 'High'

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.String(10), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

    product = db.relationship('Product', backref=db.backref('orders', lazy=True))

    def __init__(self, product_id, quantity, order_date, total_amount):
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date
        self.total_amount = total_amount

    def __repr__(self):
        return f'<Order {self.id} - Product {self.product_id}>'

