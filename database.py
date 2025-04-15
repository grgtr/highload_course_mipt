from flask_sqlalchemy import SQLAlchemy
import os

# Создаем экземпляр SQLAlchemy без привязки к приложению Flask пока
db = SQLAlchemy()

# Определяем путь к базе данных в папке 'instance'
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DB_PATH = os.path.join(BASE_DIR, 'instance', 'calculator.db')
# DB_URI = 'sqlite:///' + DB_PATH

# Функция для инициализации базы данных с приложением Flask
def init_db(app):
    # Убедимся, что папка 'instance' существует
    instance_path = os.path.join(app.root_path, 'instance')
    os.makedirs(instance_path, exist_ok=True)

    db_path = os.path.join(instance_path, 'calculator.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Отключаем отслеживание для экономии ресурсов
    db.init_app(app) # Инициализируем db с нашим Flask приложением

    with app.app_context():
        print(f"Database will be created at: {db_path}")
        db.create_all() # Создаем таблицы, если их нет