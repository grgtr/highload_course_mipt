## Как запустить проект?

1. Клонируйте этот репозиторий и перейдите в папку с ним:
```bash
git clone https://github.com/grgtr/highload_course_mipt.git
cd highload_course_mipt
```

2. Создайте и активируйте python virtual environment:
```bash
mkdir venv
cd venv
python -m venv .
source bin/activate

cd ..
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите flask app:
```bash
python app.py
```
Можете посмотреть UI по адресу http://localhost:8080

5. Запустите нагрузочное тестирование:
```bash
locust -f load_test.py
```
Перейдите в UI по адресу http://localhost:8089 и создайте нагрузочное тестирование (укажите кол-во пользователей, а в строке Host укажите http://127.0.0.1:8080)
