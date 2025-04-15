from locust import HttpUser, task, between
import random
from datetime import datetime, timedelta

class DestinyApiUser(HttpUser):
    wait_time = between(1, 3)  # Случайное время между запросами (от 1 до 3 секунд)

    @task
    def calculate_destiny_number(self):
        # Сгенерировать случайную дату рождения
        random_days = random.randint(0, 365 * 30)  # за последние 30 лет
        random_date = datetime.today() - timedelta(days=random_days)
        dob_str = random_date.strftime("%Y-%m-%d")

        # Отправить POST-запрос на API
        with self.client.post(
            "/api/calculate",
            json={"dob": dob_str},
            catch_response=True,
        ) as response:
            # Проверить, что ответ пришел успешно
            if response.status_code != 200:
                response.failure(f"Ошибка API, статус {response.status_code}")
            else:
                try:
                    result = response.json()
                    # Дополнительная проверка формата ответа (опционально)
                    if "destiny_number" not in result:
                        response.failure("Отсутствует destiny_number в ответе API")
                except ValueError:
                    response.failure("Невозможно распарсить JSON-ответ")

