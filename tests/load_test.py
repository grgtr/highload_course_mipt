from locust import HttpUser, task, between, events
import random
from datetime import datetime, timedelta
import psutil
import threading
import time

# Флаг для управления мониторинговым потоком
monitor_thread_running = True

def monitor_system(environment):
    """
    Фоновая функция, которая каждые 1-2 секунды выводит метрики:
    - Использование CPU (в %)
    - Использование памяти (в %)
    - Текущий throughput (requests/s) из статистики Locust

    Аргументы:
        environment (locust.env.Environment): окружение Locust
    """
    global monitor_thread_running

    while monitor_thread_running:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent

        if environment.runner and environment.runner.stats.total:
            current_rps = environment.runner.stats.total.current_rps
        else:
            current_rps = 0

        print(f"[SYSTEM METRICS] CPU: {cpu_usage:.1f}%, Memory: {memory_usage:.1f}%, Throughput: {current_rps:.2f} req/s")
        time.sleep(1) # Кратковременная задержка (учитывается уже внутри cpu_percent)


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    При старте теста запускается фоновой поток мониторинга,
    который выводит системные метрики и throughput.

    Аргументы:
        environment (locust.env.Environment): окружение Locust.
    """
    global monitor_thread_running
    monitor_thread_running = True
    t = threading.Thread(target=monitor_system, args=(environment,))
    t.daemon = True
    t.start()
    environment.monitor_thread = t


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    При остановке теста останавливатся фоновый поток.
    """
    global monitor_thread_running
    monitor_thread_running = False
    if hasattr(environment, "monitor_thread"):
        environment.monitor_thread.join()


class DestinyApiUser(HttpUser):
    """
    Тестовый пользователь, выполняющий запросы к API расчета числа судьбы.

    Аргументы:
        HttpUser (locust.HttpUser)
    """
    wait_time = between(1, 3)  # Случайное время между запросами (от 1 до 3 секунд)

    @task
    def calculate_destiny_number(self):
        """
        Отправляет POST-запрос с случайной датой рождения на API `/api/calculate`.
        Проверяет корректность ответа.
        """
        dob_str = self._generate_random_dob()

        with self.client.post(
            "/api/calculate",
            json={"dob": dob_str},
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"Ошибка API, статус {response.status_code}")
            else:
                try:
                    result = response.json()
                    if "destiny_number" not in result:
                        response.failure("Отсутствует destiny_number в ответе API")
                except ValueError:
                    response.failure("Невозможно распарсить JSON-ответ")

    @staticmethod
    def _generate_random_dob():
        """
        Генерирует случайную дату рождения за последние 30 лет.

        Возвращает:
            str: дата в формате 'ГГГГ-ММ-ДД'
        """
        days_ago = random.randint(0, 365 * 30)
        random_date = datetime.today() - timedelta(days=days_ago)
        return random_date.strftime("%Y-%m-%d")
