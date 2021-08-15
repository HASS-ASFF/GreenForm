from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

class MembreForm(ModelForm):
    class Meta:
        model = Membre
        fields = '__all__'
        exclude = ['user']

class PersonneForm(ModelForm):
    class Meta:
        model = Personne
        fields = '__all__'
        exclude = ['qr_code']


class CentreForm(ModelForm):
    class Meta:
        model = Centre_formation
        fields = '__all__'
        exclude = ['qr_code']


class AbonnementForm(ModelForm):
    class Meta:
        model = Adherent
        fields = '__all__'
       

class ActiviteForm(ModelForm):
    class Meta:
        model = Activite
        fields = '__all__'

class PartenaireForm(ModelForm):
    class Meta:
        model = Partenaire
        fields = '__all__'

class EtablissementForm(ModelForm):
    class Meta:
        model = Etablissement
        fields = '__all__'