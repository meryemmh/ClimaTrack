from os import name
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('',views.home , name='home'),
    path('myData/',views.dht11 , name='dht11'),
    path('myGet/',api.Mylist,name='getList'),
    path('apiPost/',api.DhtViews.as_view(),name='addList'),
    path('myGraph/<int:id>',views.dhtplot , name='plot'),
    path('about/',views.about,name='about'),
    path('services/',views.service,name="services"),
    path('contact/',views.contact,name="contact"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.user_logout,name="logout"),
    path('register/',views.registration,name='register'),
    path('userspace/',views.userspace,name='userspace'),
    path('addfridge/',views.addfridge,name='addfridge'),
    path('listfridges/',views.fridges , name='listfridges'),
    path('deletefridge/<int:id>',views.deletefridge,name='deletefridge'),
    path('editfridge/<int:id>/',views.editfridge,name='editfridge'),
    path('listassets/<int:id>/',views.assets , name='listassets'),
    path('supsettings/',views.addsupsettings , name='supsettings'),
    path('csettings/',views.ss , name='csettings'),
    path('deletedevice/<int:id>',views.deletedevice,name='deletedevice'),
    path('editdevice/<int:id>/',views.editdevice,name='editdevice'),
    path('adddevice/',views.adddevice , name='adddevice'),
    path('listdevices/',views.devices,name="deviceslist"),
    path('deletesuppsettings/<int:id>',views.deletesuppsetting,name='deletess'),
    path('myGraph/<int:id>/<str:dtd>/<str:dtf>',views.dhtplotwithdaterange , name='plotrange'),
    path('csv/', views.exp_csv, name = 'exp_csv')
    # path('addtelemtry/',views.addtelemtry , name='addtelemtry'),
]