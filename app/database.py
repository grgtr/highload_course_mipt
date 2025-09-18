from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    """
    Инициализирует соединение Flask-приложения с базой данных SQLite и создаёт необходимые таблицы.

    Аргументы:
        app (Flask): экземпляр Flask-приложения.
    """
    instance_path = os.path.join(app.root_path, 'instance')
    os.makedirs(instance_path, exist_ok=True)

    db_path = os.path.join(instance_path, 'calculator.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) 

    with app.app_context():
        print(f"Database will be created at: {db_path}")
        db.create_all()