from django.http import request
from django.shortcuts import render,get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import *
from .forms import *


#-------------------Dashboard views---------------------------------------------------------------------

def home(request):
    #code here
    return render(request,'dashboard/index.html')

#----------------------------------------ACTIVITY------------------------------------------------------
def activitylist(request):
    activity = Activite.objects.all()
    context = {
        'activity' : activity,
    }
    return render(request,'dashboard/activitieslist.html',context)

def save_all_act(request,form,template_name):
	data = dict()
	if request.method == "POST":
		if form.is_valid():
			form.save()
			data['form_is_valid']=True
			activity=Activite.objects.all()
			data['activitylist'] = render_to_string('dashboard/activities/activityitems.html',{'activity':activity})
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
	return save_all_act(request,form,'dashboard/activities/addactivity.html')

def modifyactivity(request,modify_id):
	activity = get_object_or_404(Activite , id=modify_id )
	if request.method == 'POST':
		form = ActiviteForm(request.POST,instance=activity)
	else:
		form = ActiviteForm(instance=activity)
	return save_all_act(request,form,'dashboard/activities/modifyactivity.html')


def deleteactivity(request,delete_id):
	data = dict()
	activity = get_object_or_404(Activite , id=delete_id)

	if request.method == 'POST':
		activity.delete()
		data['form_is_valid']=True
		activity=Activite.objects.all()
		data['activitylist'] = render_to_string('dashboard/activities/activityitems.html',{'activity':activity})
	else:
		context={
		'activity':activity,
		}
		data['html_form'] = render_to_string('dashboard/activities/deleteactivity.html',context,request=request)
	return JsonResponse(data)


#----------------------------------------MEMBRES---------------------------------------------------
def memberslist(request):
	personne = Personne.objects.all()
	centre = Centre_formation.objects.all()
    
	context = {
        'personne':personne,
		'centre':centre,
    }

	return render(request,'dashboard/memberlist.html',context)

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
				data['memberslist'] = render_to_string('dashboard/membres/centre/centreitems.html',context)
			else:
				personne=Personne.objects.all()
				context = {
					'personne': personne,
					'type':type,
				}
				data['memberslist'] = render_to_string('dashboard/membres/personne/persitems.html',context)	
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
	return save_all_memb(request,form,'dashboard/membres/personne/addpersonne.html',type="personne")

def addcentre(request):
	if request.method == 'POST':
		form = CentreForm(request.POST)
	else:
		form = CentreForm()
	return save_all_memb(request,form,'dashboard/membres/centre/addcentre.html',type="centre")

#----------------------------------------ABONNEMENTS-----------------------------------------------------
def abonnementList(request):
    abonnements = Adherent.objects.all()
    return render(request, 'dashboard/abonnementList.html',{'abonnement':abonnements})

#----------------------------------------PARTNERS-----------------------------------------------------------
def partnersList(request):
    partenaires = Partenaire.objects.all()

    return render(request, 'dashboard/partnersList.html',{'partenaires':partenaires})

#----------------------------------------MAPVIZUALISATION--------------------------------------------------
def mapVisualization(request):
    #code here
    return render(request, 'dashboard/mapVisualization.html')

#----------------------------------------QRCODE------------------------------------------------------------
def qrcode_search(request):
    #code here
    return render(request,'dashboard/rechercheqrcode.html')   


#---------------------Login and Register view -------------------------------------------------------------



def loginRegister(request):
    #code here
    return render(request, 'login_register/login_register.html')


def etablissementList(request):
    etablissements = Etablissement.objects.all()
    return render(request, 'dashboard/etablissementList.html',{'etablissement':etablissements})


#-------------------Member views ----------------------------------------------------------------------------

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