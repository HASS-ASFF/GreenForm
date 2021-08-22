from django.core import paginator
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
from .decorators import unauthenticated_user, allowed_users
from django.core.paginator import Paginator


#---------------------Login and Register view------------------------------------------------------------

@unauthenticated_user
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
			return redirect('home_membre')
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

#-------------------Dashboard Admin views---------------------------------------------------------------------

def home_admin(request):
    #code here
    return render(request,'dashboard_admin/index.html')

def profil_admin(request):
    #code here
    return render(request,'dashboard_admin/profil.html')

def setting_admin(request):
    #code here
    return render(request,'dashboard_admin/setting.html')

#----------------------------------------ACTIVITY------------------------------------------------------

def activitylist(request):
	activity = Activite.objects.all()
	paginator = Paginator(activity,4)
	pages = request.GET.get('page')
	page_obj = paginator.get_page(pages)

	context = {
        'activity' : page_obj,
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


#----------------------------------------MEMBRES---------------------------------------------------
def memberslist(request):
	personne = Personne.objects.all()
	paginator_pers = Paginator(personne,4)
	pages_p = request.GET.get('page')
	page_pers = paginator_pers.get_page(pages_p)

	centre = Centre_formation.objects.all()
	paginator_centr = Paginator(centre,4)
	pages_c = request.GET.get('page')
	page_centr = paginator_centr.get_page(pages_c)

	context = {
        'personne':page_pers,
		'centre':page_centr,
    }

	return render(request,'dashboard_admin/memberlist.html',context)

def save_all_memb(request,form,template_name,type):
	data = dict()
	if request.method == "POST":
		if form.is_valid():
			form.save()
			data['form_is_valid']=True
			context = {}
			if type == "center":
				centre=Centre_formation.objects.all()
				context = {
					'centre': centre,
					'type':type,
				}
				data['memberslist'] = render_to_string('dashboard_admin/membres/centre/centreitems.html',context)
			else:
				personne=Personne.objects.all()
				context = {
					'personne': personne,
					'type':type,
				}
				data['memberslist'] = render_to_string('dashboard_admin/membres/personne/persitems.html',context)	
	else:
		data['form_is_valid']=False
	
	context={
		'form': form,
	}
	data['html_form'] = render_to_string(template_name,context,request)
	return JsonResponse(data)

def addpersonne(request):
	if request.method == 'POST':
		form = PersonneForm(request.POST)
	else:
		form = PersonneForm()
	return save_all_memb(request,form,'dashboard_admin/membres/personne/addpersonne.html',type="personne")

def addcentre(request):
	if request.method == 'POST':
		form = centreFormationForm(request.POST)
	else:
		form = centreFormationForm()
	return save_all_memb(request,form,'dashboard_admin/membres/centre/addcentre.html',type="centre")

#----------------------------------------ABONNEMENTS-----------------------------------------------------
def abonnementList(request):
	abonnements = Adherent.objects.all()
	paginator = Paginator(abonnements,4)
	pages = request.GET.get('page')
	page_obj = paginator.get_page(pages)

	return render(request, 'dashboard_admin/abonnementList.html',{'abonnement':page_obj})

#----------------------------------------PARTNERS-----------------------------------------------------------
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

#----------------------------------------MAPVIZUALISATION--------------------------------------------------
def mapVisualization(request):
    #code here
    return render(request, 'dashboard_admin/mapVisualization.html')


#---------------------Etablissement view -------------------------------------------------------------

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


#------------------- Dashboard Member views ----------------------------------------------------------------------------


def home_membre(request):
	return render(request,'dashboard_membre/index.html')

def activity_show(request):
    #code here
    return render(request,'dashboard_membre/activitydetail.html')

def badge_qrcode(request):
    #code here
    return render(request,'dashboard_membre/badge.html')


#----------------------------------------QRCODE------------------------------------------------------------
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
