from django.core.management.base import BaseCommand
import random
from django.contrib.auth.models import User
from robots.models import RegisteredModel, Robot
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Создать суперпользователя и зарегистрированные модели с роботами'

    def handle(self, *args, **kwargs):
        # 1. Создание суперпользователя
        username = "test"
        email = "test@mail.com"
        password = "1234Test"

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"Superuser created: username={username}, email={email}")
        else:
            print(f"Superuser already exists: username={username}")

        # 2. Данные для RegisteredModel и роботов
        data = [
            {"model_name": "R2", "version": "D2"},
            {"model_name": "T", "version": "800"},
            {"model_name": "C-3PO", "version": "1.0"},
        ]

        created_robots = []
        for item in data:
            model_name = item["model_name"]
            version = item["version"]

            # Создаём или получаем RegisteredModel
            registered_model, created = RegisteredModel.objects.get_or_create(
                model_name=model_name,
                version=version
            )

            # Создаём роботов для RegisteredModel
            for _ in range(5):
                naive_datetime = datetime.now() - timedelta(days=random.randint(1, 365))
                aware_datetime = make_aware(naive_datetime)  # Преобразуем в aware datetime
                robot = Robot.objects.create(registered_model=registered_model,
                                             created=aware_datetime)
                created_robots.append(robot)

