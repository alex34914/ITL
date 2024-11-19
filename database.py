# database.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db

def create_app() -> Flask:
    """
    Создает и настраивает экземпляр Flask приложения.
    :return: Экземпляр Flask приложения
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
    db.init_app(app)  
    migrate = Migrate(app, db)  
    return app
