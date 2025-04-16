from flask import Flask, request, jsonify, render_template, flash
from app.database import init_db, db
from app.models import CalculationLog
from prometheus_flask_exporter import PrometheusMetrics
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'your_very_secret_key_here'

# Инициализация мониторинга
metrics = PrometheusMetrics(app)

# Инициализация базы данных
init_db(app)


def calculate_destiny_number(dob_str: str) -> int | None:
    """
    Рассчитывает число судьбы на основе даты рождения.

    Аргументы:
        dob_str (str): Дата рождения в формате 'ГГГГ-ММ-ДД'.

    Возвращает:
        int | None: Число судьбы или None в случае ошибки.
    """
    try:
        digits_str = ''.join(filter(str.isdigit, dob_str))
        if len(digits_str) != 8:
            logging.error(f"Неверный формат даты: '{dob_str}'")
            return None

        destiny_sum = sum(int(digit) for digit in digits_str)
        logging.info(f"Расчет для '{dob_str}': Строка цифр='{digits_str}', Сумма={destiny_sum}")
        return destiny_sum
    
    except ValueError:
        logging.error(f"Ошибка преобразования в число для даты: {dob_str}")
        return None
    except Exception as e:
        logging.error(f"Непредвиденная ошибка при расчете для '{dob_str}': {e}")
        return None


def save_calculation(dob: str, destiny_number: int) -> None:
    """
    Сохраняет результат расчёта числа судьбы в базу данных.

    Аргументы:
        dob (str): Дата рождения.
        destiny_number (int): Число судьбы.
    """
    try:
        log_entry = CalculationLog(dob_input=dob, destiny_number=destiny_number)
        db.session.add(log_entry)
        db.session.commit()
        logging.info(f"Запись сохранена в БД: {log_entry}")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Ошибка сохранения в БД: {e}")


# API
@app.route('/api/calculate', methods=['POST'])
def api_calculate_destiny():
    """
    API для расчёта числа судьбы.

    Аргументы:
        JSON: {"dob": "YYYY-MM-DD"}

    Возвращает:
        JSON: {"destiny_number": N} или {"error": "сообщение"}
    """
    if not request.is_json:
        return jsonify({"error": "Запрос должен быть в формате JSON"}), 400

    data = request.get_json()
    dob = data.get('dob')

    if not dob:
        return jsonify({"error": "Отсутствует поле 'dob' в запросе"}), 400

    logging.info(f"API запрос получен: dob='{dob}'")

    destiny_number = calculate_destiny_number(dob)

    if destiny_number is None:
        return jsonify({"error": "Неверный формат даты. Ожидается ГГГГ-ММ-ДД."}), 400

    save_calculation(dob, destiny_number)
    return jsonify({"destiny_number": destiny_number}), 200


# UI
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Отображает главную страницу с формой и результатами расчёта.
    """
    if request.method == 'POST':
        dob = request.form.get('dob')

        if not dob:
            flash("Пожалуйста, введите дату рождения.", "error")
            return render_template('index.html')

        logging.info(f"Запрос из формы: dob='{dob}'")
        destiny_number = calculate_destiny_number(dob)

        if destiny_number is not None:
            save_calculation(dob, destiny_number)
            return render_template('index.html', destiny_number=destiny_number, dob_submitted=dob)
        else:
            flash("Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД.", "error")

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)