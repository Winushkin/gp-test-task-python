from locust import HttpUser, task, between
import random
from datetime import datetime, timedelta, timezone

class DeviceUser(HttpUser):
    """Симулирует пользователя, работающего с API устройств"""
    wait_time = between(1, 3)  # Ждёт 1-3 сек между запросами

    def on_start(self):
        """Инициализация перед запуском"""
        self.user_id = random.randint(1000, 9999)
        
        # Отправляем POST-запрос и сохраняем ответ в переменную
        response = self.client.post(
            "/api/devices/", 
            json={
                "user_id": self.user_id, 
                "name": f"Test Device by user {self.user_id}"
            }
        )
        
        # Проверяем, что запрос выполнился успешно и получен JSON
        if response.status_code == 201:
            try:
                # Извлекаем device_id из тела ответа
                response_data = response.json()
                self.device_id = response_data.get("id")
                print(f"Устройство создано с ID: {self.device_id}")
            except ValueError:
                print("Сервер вернул ответ, но не в формате JSON")
                    


    @task(5)
    def add_measurement(self):
        """Добавить измерение (вес: 5)"""
        measurement = {
            "x": random.uniform(-100, 100),
            "y": random.uniform(-100, 100),
            "z": random.uniform(-100, 100)
        }
        self.client.post(
            f"/api/devices/{self.device_id}/measurements",
            json=measurement
        )

    @task(2)
    def get_measurements(self):
        """Получить измерения (вес: 2)"""
        self.client.get(f"/api/devices/{self.device_id}/measurements")

    @task(3)
    def get_statistics(self):
        """Получить статистику (вес: 3)"""
        self.client.get(f"/api/devices/{self.device_id}/statistics")

    @task(1)
    def get_statistics_with_period(self):
        """Получить статистику за период"""
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=7)
        
        params = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
        self.client.get(
            f"/api/devices/{self.device_id}/statistics",
            params=params
        )

    @task(1)
    def list_devices(self):
        """Получить список устройств"""
        self.client.get("/api/devices/")

    @task(1)
    def health_check(self):
        """Проверка здоровья сервиса"""
        self.client.get("/health")


class UserStatisticsUser(HttpUser):
    """Симулирует пользователя, получающего статистику по своим устройствам"""
    wait_time = between(2, 5)

    def on_start(self):
        """Инициализация"""
        # Создаём пользователя
        response = self.client.post(
            "/api/users/",
            json={
                "name": f"Test User {random.randint(1000, 9999)}",
                "email": f"user_{random.randint(100000, 999999)}@test.com"
            }
        )
        if response.status_code == 200:
            self.user_id = response.json()["id"]
        else:
            self.user_id = 1  # Fallback

    @task(3)
    def get_user_statistics(self):
        """Получить статистику пользователя"""
        self.client.get(f"/api/users/{self.user_id}/statistics")

    @task(1)
    def get_user_info(self):
        """Получить информацию о пользователе"""
        self.client.get(f"/api/users/{self.user_id}")


# Команда для запуска тестов:
# locust -f tests/locustfile.py --host=http://localhost:8000