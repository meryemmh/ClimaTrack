
import time
from django.apps import AppConfig
import sys

import myapp




class MyappConfig(AppConfig):
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    
   
    
    
#     def ready():
        
#         if 'runserver' not in sys.argv:
#             print("server down")
#         else:
               
#             from .models import Dht11
#             asset = Dht11.objects.select_related('asset').order_by('-id').first()
                
#             print(str(asset.dt)+" / "+str(asset.id))
                   
#             time.sleep(10)
     
#         # you must import your modules here 
#         # to avoid AppRegistryNotReady exception 
#         # from .models import MyModel 
#         # startup code here  
        

# while True:
#     MyappConfig.ready()




    
    
        


   

    

    