from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Product(db.Model):
    """
    Модель для представления продукта.
    :param name: Название продукта
    :param category: Категория продукта (необязательное поле)
    :param price: Цена продукта
    :param stock: Количество продукта в наличии
    :param description: Описание продукта (необязательное поле)
    """
    __tablename__ = 'products'
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(255), nullable=False)
    category: str = db.Column(db.String(255), nullable=True)
    price: float = db.Column(db.Float, nullable=False)
    stock: int = db.Column(db.Integer, nullable=False)
    description: str = db.Column(db.Text, nullable=True)

    def __init__(self, name: str, category: str, price: float, stock: int, description: str = None):
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.description = description

    def __repr__(self) -> str:
        """
        Возвращает строковое представление экземпляра Product.
        :return: Строковое представление продукта
        """
        return f'<Product {self.name}>'

    def price_category(self) -> str:
        """
        Метод для категоризации цены продукта.
        :return: Категория цены ('Low', 'Medium' или 'High')
        """
        if self.price < 1000:
            return 'Low'
        elif 1000 <= self.price <= 10000:
            return 'Medium'
        else:
            return 'High'


class Order(db.Model):
    """
    Модель для представления заказа.
    :param product_id: Идентификатор продукта
    :param quantity: Количество заказанного товара
    :param order_date: Дата заказа
    :param total_amount: Общая сумма заказа
    """
    __tablename__ = 'orders'
    id: int = db.Column(db.Integer, primary_key=True)
    product_id: int = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity: int = db.Column(db.Integer, nullable=False)
    order_date: str = db.Column(db.String(10), nullable=False)
    total_amount: float = db.Column(db.Float, nullable=False)
    product = db.relationship('Product', backref=db.backref('orders', lazy=True))

    def __init__(self, product_id: int, quantity: int, order_date: str, total_amount: float):
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date
        self.total_amount = total_amount

    def __repr__(self) -> str:
        """
        Возвращает строковое представление экземпляра Order.
        :return: Строковое представление заказа
        """
        return f'<Order {self.id} - Product {self.product_id}>'