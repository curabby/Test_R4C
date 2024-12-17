from django import forms
from .models import Robot


class ProductForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']
