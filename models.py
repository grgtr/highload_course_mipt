from database import db
from datetime import datetime

class CalculationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dob_input = db.Column(db.String(10), nullable=False) # Дата рождения как строка ГГГГ-ММ-ДД
    destiny_number = db.Column(db.Integer, nullable=False)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CalculationLog {self.dob_input} -> {self.destiny_number}>'

