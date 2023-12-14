from django.db.models import fields
from rest_framework import serializers
from .models import Dht11, Fridge

class Dht11serialize(serializers.ModelSerializer):
    class Meta:
        model = Dht11
        fields = "__all__"

class Fridgeserialize(serializers.ModelSerializer):
    class Meta:
        model = Fridge
        fields = "__all__"