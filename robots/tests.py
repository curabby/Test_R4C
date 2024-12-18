from django.test import TestCase, override_settings
from robots.models import RegisteredModel, Robot
from customers.models import Customer
from orders.models import PreOrder
from django.core import mail


class RobotSignalTestCase(TestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def setUp(self):
        print("Настройка тестовых данных...")
        self.model = RegisteredModel.objects.create(model_name="R2", version="D2")
        self.customer = Customer.objects.create(email="customer@example.com")
        self.preorder = PreOrder.objects.create(
            customer=self.customer,
            registered_model=self.model,
            is_ordered=False
        )
        print(f"Предварительный заказ создан для клиента: {self.customer.email}")

    def test_notify_customer_on_robot_availability(self):
        print("Создание экземпляра робота...")
        Robot.objects.create(
            registered_model=self.model,
            created="2024-12-12 23:59:59"
        )

        # Проверяем outbox
        print(f"Outbox size: {len(mail.outbox)}")
        for email in mail.outbox:
            print(f"Email sent to: {email.to}, Subject: {email.subject}")

        self.assertEqual(len(mail.outbox), 1)  # Проверяем, что письмо отправлено
        self.assertIn("Ваш робот теперь в наличии", mail.outbox[0].subject)
        self.assertIn(self.customer.email, mail.outbox[0].to)