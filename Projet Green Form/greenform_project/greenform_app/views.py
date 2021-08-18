from django.shortcuts import render
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users

#-------------------Dashboard views

@login_required(login_url='loginRegister')
@allowed_users(allowed_roles=['administrateur'])
def home(request):
	#code here
	return render(request,'dashboard/index.html')

@login_required(login_url='loginRegister')
def activitylist(request):
	#code here
	return render(request,'dashboard/activitieslist.html')

@login_required(login_url='loginRegister')
def memberslist(request):
	 #code here
	 return render(request,'dashboard/memberlist.html')

@login_required(login_url='loginRegister')
def abonnementList(request):
	#code here
	return render(request, 'dashboard/abonnementList.html')

@login_required(login_url='loginRegister')
def partnersList(request):
	#code here
	return render(request, 'dashboard/partnersList.html')

@login_required(login_url='loginRegister')
def mapVisualization(request):
	#code here
	return render(request, 'dashboard/mapVisualization.html')


#---------------------Login and Register view 

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
			return redirect('home')
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

@login_required(login_url='loginRegister')
def etablissementList(request):
	#code here
	return render(request, 'dashboard/etablissementList.html')


#-------------------Member views 
@login_required(login_url='loginRegister')

def personnal_profil(request):
	#code here
	return render(request,'membres/profil.html')


@login_required(login_url='loginRegister')
def activity_show(request):
	#code here
	return render(request,'membres/activity.html')


@login_required(login_url='loginRegister')
def payment_info(request):
	#code here
	return render(request,'membres/payment.html')

@login_required(login_url='loginRegister')
def qrcode_info(request):
	#code here
	return render(request,'membres/qr_code.html')