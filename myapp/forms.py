from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms import fields
from django.forms.models import ModelForm
from django.http import request

from myapp.models import Asset, Dht11, Fridge, Suppsettings

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','email','password1','password2')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class FridgeForm(ModelForm):
    class Meta:
        model=Fridge
        fields ="__all__"

class AssetForm(ModelForm):
    class Meta:
        model=Dht11
        fields ="__all__"

class SuppsettingsForm(ModelForm):
    class Meta:
        model=Suppsettings
        fields ="__all__"

class DeviceForm(ModelForm):
    class Meta:
        model=Asset
        fields="__all__"

# class TelemetryForm(ModelForm):
#     class Meta:
#         model=Telemtry
#         fields="__all__"