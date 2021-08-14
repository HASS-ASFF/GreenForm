from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),

    path('activities-list/',activitylist,name='activitylist'),
    path('activities-add',addactivity,name='addactivity'),
    path('activities-modify/<str:modify_id>',modifyactivity,name='modifyactivity'),
    path('activities-delete/<str:delete_id>',deleteactivity,name='deleteactivity'),

    path('members-list/',memberslist,name='memberslist'),
    path('personne-add',addpersonne,name='addpersonne'),
    path('centre-add',addcentre,name='addcentre'),

    path('abonnements-list/',abonnementList,name='abonnementList'),
    path('qr-code-search/',qrcode_search,name='qrcodesearch'),
    path('partenaires/',partnersList,name='partnersList'),
    path('map-vizualisation/',mapVisualization,name='mapVisualization'),
    path('etablissements-list/',etablissementList,name='etablissementList'),
    path('profil/',personnal_profil,name='profil'),
    path('activities-list/',activity_show,name='activities'),
    path('payment/',payment_info,name='payment'),
    path('qr-code/',qrcode_info,name='qrcode'),
    path('login-register/',loginRegister,name='loginRegister'),
    
]