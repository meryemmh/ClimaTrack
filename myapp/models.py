from django.db import models
from django.db.models.fields import CharField
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Fridge(models.Model):
    nom = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    creation = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="fridges", verbose_name="User",
                               null=True, default=None)

#return name in fk
    def __str__(self):
         return self.nom
        

class Asset(models.Model):
    name= models.CharField(max_length=255,null=True)
    location = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    fridge = models.ForeignKey(Fridge,on_delete=models.CASCADE, related_name="assets",verbose_name="Fridge", default=None)
    min_critical_telemetry = models.FloatField(null=False, default=None)
    max_critical_telemetry = models.FloatField(null=False, default=None)
    max_severe_telemetry = models.FloatField(null=False, default=None)
    min_severe_telemetry = models.FloatField(null=False, default=None)
    
    def __str__(self):
        return self.name

class Dht11(models.Model):
    temp = models.FloatField(null=True)
    hum = models.FloatField(null=True)
    dt = models.DateTimeField(auto_now_add=True, null=True)
    asset = models.ForeignKey(Asset,on_delete=models.CASCADE, related_name="dht11s",verbose_name="Asset", default=None)
    
     #return id in fk
    def __str__(self):
         return str(self.id)

class Suppsettings(models.Model):
    telegram_token = models.CharField(max_length=255, null=True)
    telegram_reception_id = models.CharField(max_length=255,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="suppsettings", verbose_name="User",
                               null=True, default=None)


# class Role(models.Model):
#     roles = [
#         (TS,'Technical Specialist'),
#         (DR,'Department Responsbale'),
#         (SR,'Site Responsable'),
#         (FR,'Facility Responsable')
#         ]
#     role = models.CharField(max_length=50,choices=roles,unique=True,default=TS)
#     priority = models.PositiveSmallIntegerField(verbose_name="Priorité")

#     def __str__(self):
#         return self.role
# class CustomUser(AbstractUser):
#     notified = models.BooleanField(default=True,null=False)
#     telegram_id = models.PositiveIntegerField(null=True,blank=True)
#     role = models.ForeignKey(Role,on_delete=models.CASCADE,verbose_name="Role", default=None, null=True)
#     fridges = models.ManyToManyField(Fridge,related_name="fridges",verbose_name="fridges",blank=True)
    
# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,verbose_name="User")
#     role = models.ForeignKey(Role,on_delete=models.CASCADE,verbose_name="Role")
#     # agencies = models.ManyToManyField(Agency,related_name="agences",verbose_name="Agence(s)")
#     assets = models.ManyToManyField(Asset,related_name="assets",verbose_name="Agence(s)")

