from django.contrib import admin
from .models import Asset, Dht11, Fridge, Suppsettings

# Register your models here.

admin.site.register(Dht11)
admin.site.register(Fridge)
admin.site.register(Asset)
admin.site.register(Suppsettings)