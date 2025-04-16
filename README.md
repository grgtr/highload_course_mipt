## Отчеты о проделанной работе:
- Отчет о тестировании: https://docs.google.com/document/d/16bRTDjW6HAtdDSNdXT9NzLpkXr9X_xw6N5REK_QQyLo/edit?usp=sharing
- Отчет об архитектуре и проделанной работе: https://docs.google.com/document/d/1xSWsy8kfnXe-1mEEOlKQdsjrrk3qjmmZJo3KXv1Sl30/edit?usp=sharing



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

## Запуск через docker

1) Без нагрузочного тестирования (`http://localhost:8080`)
```bash
docker-compose up --build
```
2) Вариант с нагрузочным тестированием (`http://localhost:8089`)
```bash
docker-compose --profile test up --build
```

