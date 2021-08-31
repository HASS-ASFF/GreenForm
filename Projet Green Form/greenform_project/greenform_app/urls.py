from django.urls import path
from .views import *

urlpatterns = [
    
    #-------------------- ADMIN DAHSBOARD
    path('',home,name='index'),
    
    path('login-register/',loginRegister,name='loginRegister'),
    path('logout/', logoutUser , name="logout"),
    path('profil/',profil_admin,name='profil'),
    path('profil/reset-password', resetPassword, name='resetPassword'),

    path('activities-list/',activitylist,name='activitylist'),
    path('activities-add',addactivity,name='addactivity'),
    path('activities-modify/<str:modify_id>',modifyactivity,name='modifyactivity'),
    path('activities-delete/<str:delete_id>',deleteactivity,name='deleteactivity'),
    path('export/activite', exportetactivity, name='export_activite'),

    path('members-list/',memberslist,name='memberslist'),
    #path('personne-add/',addpersonne,name='addpersonne'),
    path('centre-add/',addcentre,name='addcentre'),
    #path('personne-modify/<str:modify_id>',modifypersonne,name='modifypersonne'),
    path('centre-modify/<str:modify_id>',modifycentre,name='modifycentre'),
    #path('personne-delete/<str:delete_id>',deletepers,name='deletepersonne'),
    path('centre-delete/<str:delete_id>',deletecentr,name='deletecentre'),
    path('export/membre/<str:type>', exportmembre, name='export_membre'),

    path('abonnements-list/',abonnementList,name='abonnementList'),
    path('abonnement/',abonnementPack,name='abonnementPack'),
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
    path('badge-membre/',badge_qrcode,name='badge'),
    path('myactivity/',activity_show,name="myactivity"),
    path('actdetail/<str:act_id>',actdetails,name="actdetails"),
    path('participate/<str:act_id>',Participate,name='participate'),
]