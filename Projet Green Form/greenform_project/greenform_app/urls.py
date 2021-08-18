from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('activities-list/',activitylist,name='activitylist'),
    path('members-list/',memberslist,name='memberslist'),
    path('abonnements-list/',abonnementList,name='abonnementList'),
    path('partenaires/',partnersList,name='partnersList'),
    path('map-vizualisation/',mapVisualization,name='mapVisualization'),
    path('etablissements-list/',etablissementList,name='etablissementList'),
    path('profil/',personnal_profil,name='profil'),
    path('activities-list/',activity_show,name='activities'),
    path('payment/',payment_info,name='payment'),
    path('qr-code/',qrcode_info,name='qrcode'),
    path('login-register/',loginRegister,name='loginRegister'),
    path('logout/', logoutUser , name="logout"),
    
    
]