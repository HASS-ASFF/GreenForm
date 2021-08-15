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
    

    path('partenaires/',partnersList,name='partnersList'),
    path('partenaires-add',addpartenaire,name='addpartenaire'),
    path('partenaires-modify/<str:modify_id>',modifypartenaire,name='modifypartenaire'),
    path('partenaires-delete/<str:delete_id>',deletepartenaire,name='deletepartenaire'),

    path('map-vizualisation/',mapVisualization,name='mapVisualization'),

    path('etablissements-list/',etablissementList,name='etablissementList'),
    path('etablissement-add',addetablissement,name='addetablissement'),
    path('etablissement-modify/<str:modify_id>',modifyetablissement,name='modifyetablissement'),
    path('etablissement-delete/<str:delete_id>',deleteetablissement,name='deleteetablissement'),

    path('profil/',personnal_profil,name='profil'),
    path('activities-list/',activity_show,name='activities'),
    path('payment/',payment_info,name='payment'),

    path('qr-code-search/',Search_qrcode,name='qrcodesearch'),
    path('qr-code/<str:id_membre>/<str:type>',qrcode_info,name='qrcodeinfo'),

    path('login-register/',loginRegister,name='loginRegister'),
    
]