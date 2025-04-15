from flask import Flask, request, jsonify, render_template, flash
from database import init_db, db
from models import CalculationLog
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
# Секретный ключ нужен для flash сообщений (можно использовать os.urandom(24))
app.secret_key = 'your_very_secret_key_here'

# Инициализация базы данных
init_db(app)

# --- Вспомогательная функция для расчета ---
def calculate_destiny_number(dob_str: str) -> int | None:
    """
    Рассчитывает число судьбы по строке даты рождения (ГГГГ-ММ-ДД).
    Возвращает число или None в случае ошибки формата.
    """
    try:
        # Удаляем возможные разделители '-', '.', '/'
        digits_str = ''.join(filter(str.isdigit, dob_str))
        if len(digits_str) != 8: # Ожидаем ГГГГММДД
             # Попробуем обработать ДДММГГГГ формат, если вдруг введен так
             if len(digits_str) == 8: # Проверка на всякий случай
                 # Простая проверка, что год > 1000, месяц <=12, день <=31 - грубо
                 day = int(digits_str[0:2])
                 month = int(digits_str[2:4])
                 year = int(digits_str[4:8])
                 if year < 1000 or month > 12 or day > 31:
                     logging.warning(f"Непохоже на валидную дату: {dob_str}")
                     # не прерываем, даем шанс посчитаться, если пользователь уверен
             else: # Если длина не 8 после удаления разделителей
                 logging.error(f"Неверная длина строки цифр после очистки: '{digits_str}' из '{dob_str}'")
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


# --- API Endpoint ---
@app.route('/api/calculate', methods=['POST'])
def api_calculate_destiny():
    """
    API эндпоинт для расчета числа судьбы.
    Принимает JSON: {"dob": "YYYY-MM-DD"}
    Возвращает JSON: {"destiny_number": N} или {"error": "сообщение"}
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
        return jsonify({"error": "Неверный формат даты. Ожидается ГГГГ-ММ-ДД или похожий."}), 400

    # Сохранение в базу данных
    try:
        log_entry = CalculationLog(dob_input=dob, destiny_number=destiny_number)
        db.session.add(log_entry)
        db.session.commit()
        logging.info(f"Запись сохранена в БД: {log_entry}")
    except Exception as e:
        db.session.rollback() # Откатываем изменения в случае ошибки
        logging.error(f"Ошибка сохранения в БД: {e}")
        # Можно вернуть ошибку 500, но для пользователя важнее результат расчета
        # return jsonify({"error": "Ошибка сервера при сохранении данных"}), 500
        # Просто логируем и продолжаем

    return jsonify({"destiny_number": destiny_number}), 200

# --- UI Route ---
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Отображает главную страницу с формой и результатом.
    """
    if request.method == 'POST':
        dob = request.form.get('dob')
        if not dob:
            flash("Пожалуйста, введите дату рождения.", "error")
            return render_template('index.html')

        logging.info(f"Запрос из формы: dob='{dob}'")
        destiny_number = calculate_destiny_number(dob)

        if destiny_number is not None:
             # Сохранение в базу данных (дублируем логику API для примера)
            try:
                log_entry = CalculationLog(dob_input=dob, destiny_number=destiny_number)
                db.session.add(log_entry)
                db.session.commit()
                logging.info(f"Запись из формы сохранена в БД: {log_entry}")
            except Exception as e:
                db.session.rollback()
                logging.error(f"Ошибка сохранения в БД (из формы): {e}")
                flash("Произошла ошибка при сохранении данных.", "error")

            return render_template('index.html', destiny_number=destiny_number, dob_submitted=dob)
        else:
            flash("Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД.", "error")
            return render_template('index.html', dob_submitted=dob) # Возвращаем введенное значение

    # Для GET запроса просто отображаем страницу
    return render_template('index.html')


if __name__ == '__main__':
    # Важно: debug=True НЕ использовать в продакшене!
    app.run(debug=True, host='0.0.0.0', port=5000)