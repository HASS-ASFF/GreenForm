from django.core import paginator
from django.db.models.aggregates import Max
from django.shortcuts import render,get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.http import HttpResponse
from django.core.paginator import Paginator
import folium
import xlwt
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count, Max
import json

#---------------------Login and Register view------------------------------------------------------------


def loginRegister(request):

	saved = False
	if  request.POST.get("group") == "1":
			formCentreFormation = centreFormationForm(request.POST)
			if formCentreFormation.is_valid():
						register = formCentreFormation.save()
						user_group = Group.objects.get(id=request.POST.get("group")) 
						register.groups.add(user_group)
						saved = True
	else:
		formCentreFormation = centreFormationForm()
	if  request.POST.get("group")== "2":
			formPersonne = PersonneForm(request.POST)
			if formPersonne.is_valid():
						register = formPersonne.save()
						user_group = Group.objects.get(id=request.POST.get("group")) 
						register.groups.add(user_group)	
						saved = True
	else:
		formPersonne = PersonneForm()
	if saved:
		messages.info(request, 'Votre compte a été creer avec succée ! Connectez-vous maintenant')

 
 
	if request.POST.get("sign-in"):
		username = request.POST.get('username')
		password = request.POST.get('password')
  
		user = authenticate(request,username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('index')
		else:
			messages.info(request, 'Nom d\'utilisateur ou mot de passe incorrecte')
	context = {
				'formPersonne' : formPersonne,
			 	'formCentreFormation' : formCentreFormation,
	 }
 
	return render(request, 'login_register/login_register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('loginRegister')

@unauthenticated_user
def home(request):
	
 
 
	count_member = Membre.objects.count()
	count_activity = Activite.objects.count()
	count_partners = Partenaire.objects.count()
	count_etablissement = Etablissement.objects.count()
	
	context = {
		'count_member' : count_member,
		'count_activity' : count_activity,
		'count_partners' : count_partners,
		'count_etablissement' : count_etablissement
	} 
	return render(request,'index.html', context)

#-------------------Dashboard Admin views---------------------------------------------------------------------

@unauthenticated_user
def profil_admin(request):
	member = Membre.objects.get(username=request.user.username)
	if request.method == 'POST':
		memberForm = MemberForm(request.POST, request.FILES, instance=member)
		if memberForm.is_valid():
	  
		
			memberForm.save()
			messages.info(request, 'Profil Modifié avec succée !')
		else:
			messages.error(request, 'Une erreur est survenu !')
	
		response = {
			'data_is_valid' : True
		}
		return JsonResponse(response)


	else:
		memberForm = MemberForm(instance=member)
  
  
		context = {
			'memberForm' : memberForm
		}
		return render(request,'dashboard_admin/profil.html', context)


def resetPassword(request):
	if request.method == 'POST':
		formPassword = PasswordChangeCustomForm(request.user, request.POST)
		
		if formPassword.is_valid():
			user = formPassword.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Votre mot de passe a été bien changer')
			return redirect('logout')
		else:
			messages.error(request, 'Veuillez corriger les erreurs ci dessous')
	formPassword = PasswordChangeCustomForm(request.user)
	context = {
		'formPassword' : formPassword,
	} 
	return render(request, 'dashboard_admin/reset-password.html', context)

#----------------------------------------ACTIVITY------------------------------------------------------

@unauthenticated_user
def activitylist(request):
	activity_admin = Activite.objects.all()
	activity_membre = Activite.objects.exclude(membres=request.user.id)

	paginator_membre = Paginator(activity_membre,4)
	pages_membre = request.GET.get('page')
	pages_obj_membre = paginator_membre.get_page(pages_membre)

	paginator_admin = Paginator(activity_admin,4)
	pages_admin = request.GET.get('page')
	pages_obj_admin = paginator_admin.get_page(pages_admin)

	context = {
        'activity_admin' : pages_obj_admin,
		'activity_membre' : pages_obj_membre,
    }
	return render(request,'dashboard_admin/activitieslist.html',context)

def save_all_act(request,form,template_name):
	data = dict()
	if request.method == "POST":
		if form.is_valid():
			form.save()
			data['form_is_valid']=True
			activity=Activite.objects.all()
			data['activitylist'] = render_to_string('dashboard_admin/activities/activityitems.html',{'activity':activity})
	else:
		data['form_is_valid']=False
	
	context={
		'form': form,
	}
	data['html_form'] = render_to_string(template_name,context,request)
	return JsonResponse(data)

def Participate(request,act_id):
	data = dict()
	saved = False
	activity = get_object_or_404(Activite , id=act_id )
	if request.method == 'POST':
		print('post')
		data['form_is_valid']=True
		saved = True
		activity.membres.add(Membre.objects.get(id=request.user.id))
	if saved:
		messages.info(request, 'Vous Participez desormais à cette activité !')
	else:
		print('get')
		context={
			'activity':activity,
		}
		data['html_form'] = render_to_string('dashboard_membre/participate.html',context,request=request)
	return JsonResponse(data)

def actdetails(request,act_id):
	data = dict()
	activity = get_object_or_404(Activite, id=act_id)
	membres = [m for m in Membre.objects.all() if m in activity.membres.all().exclude(id=request.user.id)]
	context={
		'activity':activity,
		'membres': membres,
	}
	data['html_form'] = render_to_string("dashboard_membre/activitydetail.html",context,request=request)
	return JsonResponse(data)


def addactivity(request):
	if request.method == 'POST':
		form = ActiviteForm(request.POST)
	else:
		form = ActiviteForm()
	return save_all_act(request,form,'dashboard_admin/activities/addactivity.html')

def modifyactivity(request,modify_id):
	activity = get_object_or_404(Activite , id=modify_id )
	if request.method == 'POST':
		form = ActiviteForm(request.POST,instance=activity)
	else:
		form = ActiviteForm(instance=activity)
	return save_all_act(request,form,'dashboard_admin/activities/modifyactivity.html')


def deleteactivity(request,delete_id):
	data = dict()
	activity = get_object_or_404(Activite , id=delete_id)

	if request.method == 'POST':
		activity.delete()
		data['form_is_valid']=True
		activity=Activite.objects.all()
		data['activitylist'] = render_to_string('dashboard_admin/activities/activityitems.html',{'activity':activity})
	else:
		context={
		'activity':activity,
		}
		data['html_form'] = render_to_string('dashboard_admin/activities/deleteactivity.html',context,request=request)
	return JsonResponse(data)

def exportetactivity(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Liste Activités.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users Data') 
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.num_format_str = 'D-MMM-YY'
	font_style.font.bold = True

	columns = ['Nom', 'Description', 'Date']
	rows = Activite.objects.all().values_list('nom','desc', 'date')
	
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 
	# Sheet body, remaining rows
	font_style = xlwt.XFStyle()

	style = xlwt.XFStyle()
	style.num_format_str = 'D-MMM-YY'
	
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			if col_num == 2:
				ws.write(row_num, col_num, row[col_num], style)
			else:
				ws.write(row_num, col_num, row[col_num], font_style)


	wb.save(response)

	return response

#----------------------------------------MEMBRES---------------------------------------------------
@unauthenticated_user
def memberslist(request):
	personne = Personne.objects.all()
	paginator_pers = Paginator(personne,4)
	pages_p = request.GET.get('pagePerson')
	page_pers = paginator_pers.get_page(pages_p)

	centre = Centre_formation.objects.all()
	paginator_centr = Paginator(centre,4)
	pages_c = request.GET.get('pageCenter')
	page_centr = paginator_centr.get_page(pages_c)

	context = {
		'personne':page_pers,
		'centre':page_centr,
	}

	return render(request,'dashboard_admin/memberlist.html',context)

def save_all_memb(request,form,template_name):
	data = dict()
	if request.method == "POST":
		if form.is_valid():
			form.save()
			data['form_is_valid']=True
		else:
			data['form_is_valid']=False
			messages.error(request, 'Something went wrong !')	
	else:	
		context={
			'form': form,
			}
		data['html_form'] = render_to_string(template_name,context,request)
	return JsonResponse(data)
#----------- PERSONNE ----------#
def addpersonne(request):
	if request.method == 'POST':
		form = PersonneForm(request.POST)
	else:
		form = PersonneForm()
	return save_all_memb(request,form,'dashboard_admin/membres/personne/addpersonne.html') 

def modifypersonne(request,modify_id):
	personne = Personne.objects.get(id=modify_id)
	if request.method == 'POST':
		form = PersonneForm(request.POST,instance=personne)
	else:
		form = PersonneForm(instance=personne)
	return save_all_memb(request,form,'dashboard_admin/membres/personne/modifypersonne.html')


def deletepers(request,delete_id):
	data = dict()
	personne = get_object_or_404(Personne , id=delete_id)

	if request.method == 'POST':
		personne.delete()
		data['form_is_valid']=True
		personne=Personne.objects.all()
		data['memberslist'] = render_to_string('dashboard_admin/membres/personne/persitems.html',{'personne':personne})
	else:
		context={
		'personne':personne,
		}
		data['html_form'] = render_to_string('dashboard_admin/membres/personne/deletepersonne.html',context,request=request)
	return JsonResponse(data) 

#----------- END PERSONNE ----------#

#----------- START CENTRE ------------#
def addcentre(request):
	if request.method == 'POST':
		form = centreFormationForm(request.POST)
		print(request.POST.get('email'))
	else:
		form = centreFormationForm()
	return save_all_memb(request,form,'dashboard_admin/membres/centre/addcentre.html')

def modifycentre(request,modify_id):
	centre = get_object_or_404(Centre_formation , id=modify_id )
	if request.method == 'POST':
		form = centreFormationForm(request.POST,instance=centre)
		print(request.POST.get('username'))
	else:
		form = centreFormationForm(instance=centre)
	return save_all_memb(request,form,'dashboard_admin/membres/centre/modifycentre.html')


def deletecentr(request,delete_id):
	data = dict()
	centre = get_object_or_404(Centre_formation , id=delete_id)

	if request.method == 'POST':
		centre.delete()
		data['form_is_valid']=True
		centre=Centre_formation.objects.all()
		data['memberslist'] = render_to_string('dashboard_admin/membres/centre/centreitems.html',{'centre':centre})
	else:
		context={
		'centre':centre,
		}
		data['html_form'] = render_to_string('dashboard_admin/membres/centre/deletecentre.html',context,request=request)
	return JsonResponse(data)


#----------- END CENTER ----------- #


def exportmembre(request,type):
	response = HttpResponse(content_type='application/ms-excel')
	

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users Data') 

	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	if type == "personne":
		columns = ['Nom', 'Prenom', 'sexe', 'Adresse','Code postal', 'Téléphone' ]
		rows = Personne.objects.all().values_list('nom', 'prenom', 'sexe', 'adresse', 'code_postal', 'num_tel')
		response['Content-Disposition'] = 'attachment; filename="Liste Personnes.xls"'
	if type == "centre":
		columns = ['Responsable', 'Nom', 'Code Postal']
		rows = Centre_formation.objects.all().values_list('responsable', 'nom_du_centre', 'code_postal')
		response['Content-Disposition'] = 'attachment; filename="Liste Centre de formation.xls"'

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)  

	font_style = xlwt.XFStyle()

	
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)

	return response

#----------------------------------------ABONNEMENTS-----------------------------------------------------
@unauthenticated_user
def abonnementList(request):
	listAdherentByAbonnement = Membre.objects.values('username', 'id').annotate(abonnement_count=Count('adherent__id_membre'), last_abonnement=Max('adherent__date_abonnement')).exclude(abonnement_count=0)	
	paginator_abonnement = Paginator(listAdherentByAbonnement,4)
	pages_abo = request.GET.get('pageAbonnement')
	page_abonnement = paginator_abonnement.get_page(pages_abo)

	context = {
		'listAdherent' : listAdherentByAbonnement,
		'page_abonnement' : page_abonnement
	}
	

	return render(request, 'dashboard_admin/abonnementList.html', context)

def exportabonnement(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Liste Adhérants.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users Data') 

	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Membre', 'Date abonnement', 'Numéro']
	rows = Adherent.objects.all().values_list('id_inscription', 'date_abonnement', 'id_abonnement')
	
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style) 

	font_style = xlwt.XFStyle()

	
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)

	return response

def abonnementPack(request):
	
	if request.method == "POST":
		adherentForm = AdherantForm(request.POST)
		if adherentForm.is_valid():
			adherentForm.save()
			messages.info(request, 'Votre abonnement a été bien effectué !')
		else:
			messages.error(request, 'Something went wrong !')
	
	else:
		adherentForm = AdherantForm()
	
	listAbonnementByAdherent = Adherent.objects.filter(id_membre = request.user.id)
 
	paginator_abonnement = Paginator(listAbonnementByAdherent,4	)
	pages_abo = request.GET.get('pagePacks')
	page_adherent = paginator_abonnement.get_page(pages_abo)

	
	context = {
	 'adherentForm' : adherentForm,
	#  'listAbonnementByAdherent' : listAbonnementByAdherent,
 	 'page_adherent' : page_adherent
	 }
	return render(request, 'dashboard_admin/abonnementPacks.html', context)

def countAbonnement(request):
	count_abonnement = Adherent.objects.filter(id_membre = request.user.id).count()
	context = {
     	'count_abonnement' : count_abonnement
    }
	return context

#----------------------------------------PARTNERS-----------------------------------------------------------
@unauthenticated_user
def partnersList(request):
	partenaires = Partenaire.objects.all()
	paginator = Paginator(partenaires,4)
	pages = request.GET.get('page')
	page_obj = paginator.get_page(pages)

	return render(request, 'dashboard_admin/partnersList.html',{'partenaires':page_obj})

def save_all_part(request,form,template_name):
	data = dict()
	if request.method == "POST":
		if form.is_valid():
			form.save()
			data['form_is_valid']=True
			partenaire=Partenaire.objects.all()
			data['partnersList'] = render_to_string('dashboard_admin/partenaires/partiems.html',{'partenaire':partenaire})
	else:
		data['form_is_valid']=False
	
	context={
		'form': form,
	}
	data['html_form'] = render_to_string(template_name,context,request)
	return JsonResponse(data)

def addpartenaire(request):
	if request.method == 'POST':
		form = PartenaireForm(request.POST)
	else:
		form = PartenaireForm()
	return save_all_act(request,form,'dashboard_admin/partenaires/addpart.html')

def modifypartenaire(request,modify_id):
	partenaire = get_object_or_404(Partenaire , id=modify_id )
	if request.method == 'POST':
		form = PartenaireForm(request.POST,instance=partenaire)
	else:
		form = PartenaireForm(instance=partenaire)
	return save_all_act(request,form,'dashboard_admin/partenaires/modifypart.html')

def deletepartenaire(request,delete_id):
	data = dict()
	partenaire = get_object_or_404(Partenaire , id=delete_id)

	if request.method == 'POST':
		partenaire.delete()
		data['form_is_valid']=True
		partenaire=Partenaire.objects.all()
		data['partnersList'] = render_to_string('dashboard_admin/partenaires/partitems.html',{'partenaire':partenaire})
	else:
		context={
		'partenaire':partenaire,
		}
		data['html_form'] = render_to_string('dashboard_admin/partenaires/deletepart.html',context,request=request)
	return JsonResponse(data)

def exportpartenaire(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Liste Partenaires.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users Data')

	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Nom','Adresse','Code postal', 'Téléphone' ]
	rows = Partenaire.objects.all().values_list('nom', 'adresse', 'code_postal', 'num_tel')
	
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style) 

	font_style = xlwt.XFStyle()

	
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)

	return response

#----------------------------------------MAPVIZUALISATION--------------------------------------------------
@unauthenticated_user
def mapVisualization(request):
	map = folium.Map(location=[47,2],zoom_start=5)
	map = map._repr_html_()
	return render(request, 'dashboard_admin/mapVisualization.html',{'map':map})


#---------------------Etablissement view -------------------------------------------------------------
@unauthenticated_user
def etablissementList(request):
	etablissements = Etablissement.objects.all()
	paginator = Paginator(etablissements,4)
	pages = request.GET.get('page')
	page_obj = paginator.get_page(pages)

	return render(request, 'dashboard_admin/etablissementList.html',{'etablissement':page_obj})

def save_all_etab(request,form,template_name):
	data = dict()
	if request.method == "POST":
		if form.is_valid():
			form.save()
			data['form_is_valid']=True
			etablissement=Etablissement.objects.all()
			data['etablissementList'] = render_to_string('dashboard_admin/etablissement/etabitems.html',{'etablissement':etablissement})
	else:
		data['form_is_valid']=False
	
	context={
		'form': form,
	}
	data['html_form'] = render_to_string(template_name,context,request)
	return JsonResponse(data)

def addetablissement(request):
	if request.method == 'POST':
		form = EtablissementForm(request.POST)
	else:
		form = EtablissementForm()
	return save_all_act(request,form,'dashboard_admin/etablissement/addetablissement.html')

def modifyetablissement(request,modify_id):
	etablissement = get_object_or_404(Etablissement , id=modify_id )
	if request.method == 'POST':
		form = EtablissementForm(request.POST,instance=etablissement)
	else:
		form = EtablissementForm(instance=etablissement)
	return save_all_act(request,form,'dashboard_admin/etablissement/modifyetablissement.html')


def deleteetablissement(request,delete_id):
	data = dict()
	etablissement = get_object_or_404(Etablissement , id=delete_id)

	if request.method == 'POST':
		etablissement.delete()
		data['form_is_valid']=True
		etablissement=Etablissement.objects.all()
		data['etablissementList'] = render_to_string('dashboard_admin/etablissement/etabitems.html',{'etablissement':etablissement})
	else:
		context={
		'etablissement':etablissement,
		}
		data['html_form'] = render_to_string('dashboard_admin/etablissement/deleteetablissement.html',context,request=request)
	return JsonResponse(data)

def exportetablissement(request):
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename="Liste Etablissements.xls"'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users Data') 

	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Représentant', 'Nom', 'Type', 'Adresse','Code postal']
	rows = Etablissement.objects.all().values_list('representant','nom','type_etablissement', 'adresse', 'code_postal')
	
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style) 

	font_style = xlwt.XFStyle()

	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)

	return response

#------------------- Dashboard Member views ----------------------------------------------------------------------------
@unauthenticated_user
def activity_show(request):
    activity = Activite.objects.filter(membres=request.user.id)
    return render(request,'dashboard_membre/myactivity.html',{'activity':activity})

@unauthenticated_user
def badge_qrcode(request):

	if request.user.groups.filter(name='personne').exists():
		personne = get_object_or_404(Personne, id=request.user.id )
		centre = []
	else:
		centre = get_object_or_404(Centre_formation, id=request.user.id )
		personne = []
	context ={
		'centre':centre,
		'personne': personne,
	}
	
	return render(request,'dashboard_membre/badge.html',context)

def Gifts(request):
	return render(request,'dashboard_membre/listecadeaux.html')

#----------------------------------------QRCODE------------------------------------------------------------
@unauthenticated_user
def Search_qrcode(request):
	query = request.GET.get('query')
	
	if not query:
		personnes = Personne.objects.all()
		centre = Centre_formation.objects.all()
	else:
		personnes = Personne.objects.filter(nom__icontains=query)
		centre = Centre_formation.objects.filter(nom_du_centre__icontains=query)
		if not personnes:
			personnes = Personne.objects.filter(prenom__icontains=query) 

	paginator_pers = Paginator(personnes,4)
	pages_p = request.GET.get('page')
	page_pers = paginator_pers.get_page(pages_p)

	paginator_centr = Paginator(centre,4)
	pages_c = request.GET.get('page')
	page_centr = paginator_centr.get_page(pages_c)
	context = {
		'personne' : page_pers,
		'centre' : page_centr,
		'query':query,
	}
	return render(request,'dashboard_admin/rechercheqrcode.html',context)
	 

def qrcode_info(request,id_membre,type):
	data = dict()
	if type == "personne":
		personne = get_object_or_404(Personne , id=id_membre)
		context = {
		'membre' : personne,
		'type' : type,
		}
	else:
		centre = get_object_or_404(Centre_formation , id=id_membre)
		context = {
		'membre' : centre,
		'type' : type,
		}
	
	data['html_form'] = render_to_string('dashboard_admin/qr_code.html',context,request)
	return JsonResponse(data)
