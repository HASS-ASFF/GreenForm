from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('activities-list/',activitylist,name='activitylist'),
    path('members-list/',memberslist,name='memberslist'),

    path('profil/',personnal_profil,name='profil'),
    path('activities/',activity_show,name='activities'),
    path('payment/',payment_info,name='payment'),
    path('qr-code/',qrcode_info,name='qrcode'),
    
]