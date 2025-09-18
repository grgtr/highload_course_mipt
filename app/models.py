from app.database import db
from datetime import datetime

class CalculationLog(db.Model):
    """
    Модель ORM для хранения истории вычислений чисел судьбы по датам рождения.

    Аргументы:
        id (int): Первичный ключ записи.
        dob_input (str): Дата рождения в формате 'ГГГГ-ММ-ДД'.
        destiny_number (int): Вычисленное число судьбы.
        calculated_at (datetime): Дата и время, когда был сделан расчёт.
    """
    id = db.Column(db.Integer, primary_key=True)
    dob_input = db.Column(db.String(10), nullable=False)
    destiny_number = db.Column(db.Integer, nullable=False)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CalculationLog {self.dob_input} -> {self.destiny_number}>'

