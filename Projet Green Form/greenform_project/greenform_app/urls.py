from django.urls import path
from .views import *

urlpatterns = [
    
    #-------------------- ADMIN DAHSBOARD
    path('',home_admin,name='home_admin'),
    
    path('login-register/',loginRegister,name='loginRegister'),
    path('logout/', logoutUser , name="logout"),
    
    path('profil/',profil_admin,name='profil'),
    path('setting/',setting_admin,name='setting'),

    path('activities-list/',activitylist,name='activitylist'),
    path('activities-add',addactivity,name='addactivity'),
    path('activities-modify/<str:modify_id>',modifyactivity,name='modifyactivity'),
    path('activities-delete/<str:delete_id>',deleteactivity,name='deleteactivity'),
    path('export/activite', exportetactivity, name='export_activite'),

    path('members-list/',memberslist,name='memberslist'),
    path('export/membre/<str:type>', exportmembre, name='export_membre'),

    path('abonnements-list/',abonnementList,name='abonnementList'),
    path('export/adherant', exportabonnement, name='export_adherant'),

    path('partenaires/',partnersList,name='partnersList'),
    path('partenaires-add',addpartenaire,name='addpartenaire'),
    path('partenaires-modify/<str:modify_id>',modifypartenaire,name='modifypartenaire'),
    path('partenaires-delete/<str:delete_id>',deletepartenaire,name='deletepartenaire'),
    path('export/partenaires',exportpartenaire,name='export_part'),

    path('map-vizualisation/',mapVisualization,name='mapVisualization'),

    path('etablissements-list/',etablissementList,name='etablissementList'),
    path('etablissement-add',addetablissement,name='addetablissement'),
    path('etablissement-modify/<str:modify_id>',modifyetablissement,name='modifyetablissement'),
    path('etablissement-delete/<str:delete_id>',deleteetablissement,name='deleteetablissement'),
    path('export/etablissement',exportetablissement,name='export_etab'),
    

    path('qr-code-search/',Search_qrcode,name='qrcodesearch'),
    path('qr-code/<str:id_membre>/<str:type>',qrcode_info,name='qrcodeinfo'),

    path('login-register/',loginRegister,name='loginRegister'),

    #-------------------- MEMBRE DAHSBOARD
    path('index/',home_membre,name='home_membre'),
    path('badge-membre/',badge_qrcode,name='badge'),
]