from django.shortcuts import render
from .models import *


#-------------------Dashboard views

def home(request):
    #code here
    return render(request,'dashboard/index.html')

def activitylist(request):
    #code here
    return render(request,'dashboard/activitieslist.html')

def memberslist(request):
     #code here
     return render(request,'dashboard/memberlist.html')

#-------------------Member views 

def personnal_profil(request):
    #code here
    return render(request,'membres/profil.html')

def activity_show(request):
    #code here
    return render(request,'membres/activity.html')

def payment_info(request):
    #code here
    return render(request,'membres/payment.html')

def qrcode_info(request):
    #code here
    return render(request,'membres/qr_code.html')