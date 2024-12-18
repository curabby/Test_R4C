from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Robot
from orders.models import PreOrder


@receiver(post_save, sender=Robot)
def notify_customer_on_robot_availability(sender, instance, created, **kwargs):
    if created:
        preorders = PreOrder.objects.filter(
            registered_model=instance.registered_model,
            is_ordered=False
        )
        if preorders:
            for preorder in preorders:
                send_mail(
                    subject="Ваш робот теперь в наличии",
                    message=(
                        f"Добрый день!\n\n"
                        f"Недавно вы интересовались нашим роботом модели {instance.registered_model.model_name}, "
                        f"версии {instance.registered_model.version}.\n"
                        f"Этот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами."
                    ),
                    from_email="noreply@company.com",
                    recipient_list=[preorder.customer.email],
                )