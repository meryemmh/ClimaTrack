from django.contrib.auth.forms import UserCreationForm
from django.http.response import Http404, HttpResponse
from django.shortcuts import redirect, render
from myapp.forms import AssetForm, DeviceForm, FridgeForm, LoginForm,RegistrationForm, SuppsettingsForm
from django.contrib.auth import authenticate , login ,logout
from myapp.models import Asset, Dht11, Fridge, Suppsettings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import telepot
from django.core.mail import send_mail
import csv

gtelegram_token =''
gtelegram_chat_id =''



def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'service.html')

def contact(request):
    return render(request,'contact.html')

@login_required
def userspace(request):
    return render(request,'usertemplate/userspace.html')


def dht11(request):
    tab = Dht11.objects.all()
    s = {'tab':tab}
    return render(request,'vals.html',s)
@login_required
def dhtplot(request,id):
    grph = Dht11.objects.select_related('asset').filter(asset_id=id)
    p = {'grph':grph}
    return render(request,'plot.html',p)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request,'index.html',{'user':user})
                else:
                    return HttpResponse("404")
            else:
                return HttpResponse("500")
        else:
            form = LoginForm()
            return render(request,'login.html',{'form':form})
    else:
        form = LoginForm()
        return render(request,'login.html',{'form':form})

@login_required
def user_logout(request):
    logout(request)
    return render(request,'logout.html')

def registration(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            
            user_form.save()
           
            return render(request,'index.html')
        else: 
            return HttpResponse("404")
    else:
        user_form=RegistrationForm()
    return render(request,'register.html',{'user_form':user_form})   

@login_required
def addfridge(request):
    if request.method == "POST":
        fridge_form = FridgeForm(request.POST)
        if fridge_form.is_valid():
            fridge_form.save()
            messages.info(request,'Added Successfully !')
            fridge_form=FridgeForm()
        else: 
            return HttpResponse("404")
    else:
        fridge_form=FridgeForm()
    return render(request,'usertemplate/fridge/addfridge.html',{'fridge_form':fridge_form}) 

@login_required
def fridges(request):
    fridges = Fridge.objects.order_by('id').filter(user=request.user.id)
    s = {'fridges':fridges}


    return render(request,'usertemplate/fridge/listfridges.html',s)

@login_required
def deletefridge(request,id):
    fridge = Fridge.objects.get(id =id)
    fridge.delete()
    messages.info(request,'Deleted Successfully')
    return redirect('/listfridges')

@login_required
def editfridge(request,id):
    editfridge = Fridge.objects.get(id=id)
    editfridge_form = FridgeForm(instance=editfridge)

    if request.method == 'POST':
        editfridge_form = FridgeForm(request.POST, instance=editfridge)
        if editfridge_form.is_valid():
            editfridge_form.save()
            return redirect('/listfridges')
        else:
            return HttpResponse("404")

    return render(request,'usertemplate/fridge/editfridge.html',{'editfridge_form':editfridge_form})

@login_required
def assets(request,id):
    # '-' before id means desc
    assets = Dht11.objects.select_related('asset').order_by('-id').filter(asset_id=id)
  
    count =0 
    device=""
    message =""
    for o in assets:
        if o.temp > o.asset.max_critical_telemetry or o.temp < o.asset.min_critical_telemetry :
            count+=1
            message = "alert d'un passage de température critique "
            device = o.asset.name
       

    if count > 0:
        sendmail(count,device,message)        
        sendtelegram(count,device,message)   
      

    s = {'assets':assets}
    return render(request,'usertemplate/asset/listassets.html',s)




@login_required
def addsupsettings(request):
    cl = Suppsettings.objects.count()
    if(cl == 0):
     if request.method == "POST":
        ss_form = SuppsettingsForm(request.POST)
        if ss_form.is_valid():
            ss_form.save()

            messages.info(request,'Added Successfully !')
            return redirect("/csettings")
        else: 
            return HttpResponse("404")
     else:
        ss_form=SuppsettingsForm()
     return render(request,'usertemplate/usettings/usersettings.html',{'ss_form':ss_form}) 
    else:
      return HttpResponse("404");
  
@login_required
def ss(request):
  
    ss = Suppsettings.objects.filter(user=request.user.id)
    for sq in ss:
        gtelegram_token = sq.telegram_token
        gtelegram_chat_id  = sq.telegram_reception_id
    s = {'ss':ss}
    print(gtelegram_token , gtelegram_chat_id )
    return render(request,'usertemplate/usettings/csettings.html',s)

@login_required
def adddevice(request):
    if request.method == "POST":
        device_form = DeviceForm(request.POST)
        if device_form.is_valid():
            device_form.save()
            messages.info(request,'Added Successfully !')
            # device_form=DeviceForm()
            return redirect('/listdevices')
        else: 
            return HttpResponse("404")
    else:
        device_form=DeviceForm()
    return render(request,'usertemplate/device/adddevice.html',{'device_form':device_form}) 

@login_required
def devices(request):
    devices = Asset.objects.select_related('fridge').order_by('id')
    s = {'devices':devices}
    return render(request,'usertemplate/device/listdevices.html',s)

@login_required
def deletedevice(request,id):
    asset = Asset.objects.get(id =id)
    asset.delete()
    messages.info(request,'Deleted Successfully')
    return redirect('/listdevices')

@login_required
def editdevice(request,id):
    editdevice = Asset.objects.get(id=id)
    editdevice_form = DeviceForm(instance=editdevice)

    if request.method == 'POST':
        editdevice_form = DeviceForm(request.POST, instance=editdevice)
        if editdevice_form.is_valid():
            editdevice_form.save()
            return redirect('/listdevices')
        else:
            return HttpResponse("404")

    return render(request,'usertemplate/device/editdevice.html',{'editdevice_form':editdevice_form})


def sendtelegram(n,dev,message):
   
    #token = '5014526009:AAEhb03bYa3NDGIlfoJ1t3xhulEWlQftmeM'
    token = '5084355865:AAEONacGXOI11aou5UtdISSIGYcX_qkLzDg'
    # rece_id= "2053277412"
    rece_id= "1771754777"
    bot = telepot.Bot(token)
    # bot.sendMessage(rece_id,'la temperature dépasse la valeur normal')
    print(bot.sendMessage(rece_id,message+'la temperature dépasse la valeur normal '+str(n)+' fois . dans le capteur '+str(dev)))

def sendmail(n,dev,message):
    
          send_mail('température dépasse la normale ',
          message+'la temperature dépasse la valeur normal '+str(n)+' fois . dans le capteur '+str(dev),

          'ba2migang@gmail.com',
          ['imahrain1fcb@gmail.com','hind.belbachir103@gmail.com'],
          fail_silently=False)
        
@login_required
def deletesuppsetting(request,id):
    asset = Suppsettings.objects.get(id =id)
    asset.delete()
    messages.info(request,'Deleted Successfully')
    return redirect('/userspace')

@login_required
def dhtplotwithdaterange(request,id,dtd,dtf):
    grph = Dht11.objects.select_related('asset').filter(asset_id=id,dt__range=[dtd,dtf])
    if grph:
        p = {'grph':grph}
        return render(request,'plot.html',p)
    else:
        return HttpResponse("<div class='message alert alert-success'><strong>404 There Are No Data At This Range Of Time</strong> <a href='/listdevices' class='text-warning'>return to devices list </a>")
    
    return render(request,'plot.html',p)


@login_required
def exp_csv(request):
     obj = Dht11.objects.all()
     response = HttpResponse('text/csv')
     response['Content-Disposition'] = 'attachment; filename=DHT11.csv'
     writer = csv.writer(response)
     writer.writerow([ '','\n Temperature',  'Date'])
     studs = obj.values_list('temp', 'dt')
     for std in studs:
        writer.writerow(std)
     return response

    
   