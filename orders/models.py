from django.db import models

from customers.models import Customer
from robots.models import Robot, RegisteredModel


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot = models.OneToOneField(Robot, on_delete=models.CASCADE)
    order_date = models.DateField(blank=False, null=False)

class PreOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    registered_model = models.ForeignKey(RegisteredModel, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)