from locust import HttpUser, task, between, events
import random
from datetime import datetime, timedelta
import psutil
import threading
import time

# Глобальный флаг для управления мониторинговым потоком
monitor_thread_running = True

def monitor_system(environment):
    """
    Фоновая функция, которая каждые 1-2 секунды выводит метрики:
    - Использование CPU (в %)
    - Использование памяти (в %)
    - Текущий throughput (requests/s) из статистики Locust
    """
    global monitor_thread_running
    while monitor_thread_running:
        # Получаем процент загрузки CPU за интервал в 1 секунду
        cpu_usage = psutil.cpu_percent(interval=1)
        # Получаем процент использования виртуальной памяти
        memory_usage = psutil.virtual_memory().percent
        # Получаем текущий throughput из статистики Locust
        if environment.runner and environment.runner.stats.total:
            current_rps = environment.runner.stats.total.current_rps
        else:
            current_rps = 0
        print(f"[SYSTEM METRICS] CPU: {cpu_usage:.1f}%, Memory: {memory_usage:.1f}%, Throughput: {current_rps:.2f} req/s")
        # Кратковременная задержка (учитывается уже внутри cpu_percent)
        time.sleep(1)

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    При старте теста запускается фоновой поток мониторинга,
    который выводит системные метрики и throughput.
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
    При остановке теста останавливаем фоновый поток.
    """
    global monitor_thread_running
    monitor_thread_running = False
    if hasattr(environment, "monitor_thread"):
        environment.monitor_thread.join()

class DestinyApiUser(HttpUser):
    wait_time = between(1, 3)  # Случайное время между запросами (от 1 до 3 секунд)

    @task
    def calculate_destiny_number(self):
        # Сгенерировать случайную дату рождения за последние 30 лет
        random_days = random.randint(0, 365 * 30)
        random_date = datetime.today() - timedelta(days=random_days)
        dob_str = random_date.strftime("%Y-%m-%d")

        # Отправить POST-запрос на API /api/calculate с JSON-телом
        with self.client.post(
            "/api/calculate",
            json={"dob": dob_str},
            catch_response=True,
        ) as response:
            # Если статус не 200, зафиксировать неудачу
            if response.status_code != 200:
                response.failure(f"Ошибка API, статус {response.status_code}")
            else:
                try:
                    result = response.json()
                    # Проверяем, что в ответе присутствует ключ "destiny_number"
                    if "destiny_number" not in result:
                        response.failure("Отсутствует destiny_number в ответе API")
                except ValueError:
                    response.failure("Невозможно распарсить JSON-ответ")
