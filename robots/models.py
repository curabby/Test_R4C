from django.db import models
import uuid

# Таблица зарегистрированных моделей
class RegisteredModel(models.Model):
    model_name = models.CharField(max_length=2)
    version = models.CharField(max_length=2)

    class Meta:
        unique_together = ('model_name', 'version')  # Уникальность пары модель-версия

    def __str__(self):
        return f"{self.model_name} - {self.version}"


class Robot(models.Model):
    serial = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    registered_model = models.ForeignKey(RegisteredModel, on_delete=models.CASCADE, related_name="robots")
    created = models.DateTimeField(blank=False, null=False)
    is_distributed = models.BooleanField(default=False)

    def __str__(self):
        return f"Robot {self.registered_model} ({self.serial})"
