from django.contrib import admin
from .models import Robot, RegisteredModel



# Регистрация модели RegisteredModel
@admin.register(RegisteredModel)
class RegisteredModelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'version')
    search_fields = ('model_name', 'version')


# Регистрация модели Robot
@admin.register(Robot)
class RobotAdmin(admin.ModelAdmin):
    list_display = ('serial', 'registered_model', 'created')
    list_filter = ('registered_model', 'created')
    search_fields = ('serial', 'registered_model__model_name')
    ordering = ('-created',)