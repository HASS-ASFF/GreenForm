from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import *
from django.utils.translation import gettext_lazy as _


class MemberForm(forms.ModelForm):
    class Meta:
        model = Membre
        fields = ['username', 'email', 'image_profil']
        
        def clean_email(self):
            email = self.cleaned_data['email']
            if Personne.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    'Please use another Email, that is already taken')
            return email
        
        def save(self, commit=True):
            user = super(MemberForm, self).save(commit=False)
            
            if commit:
                user.save()
            return user
        widgets = {
                'username' : forms.TextInput(attrs={'class': 'form-control'}),
                'email' : forms.TextInput(attrs={'class':'form-control'}),
                'image_profil' : forms.FileInput(attrs={'class': 'form-control'})
        }
        
class PersonneForm(forms.ModelForm):
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput) 

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def save(self, commit=True):
        user = super(PersonneForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3 username_personne', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3 email_personne', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3 password_personne', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control password2_personne', 'placeholder': 'Repeat Password'})    
    
    class Meta:
        model = Personne
        fields = ['username', 'password' ,'email','nom','prenom', 'sexe', 'adresse', 'num_tel', 'type', 'code_postal']
        widgets = {
                'username' : forms.TextInput(attrs={'class': 'form-control username_personne'}),
                'password' : forms.PasswordInput(attrs={'class': 'form-control mb-3 password_personne'}),
                'email' : forms.TextInput(attrs={'class':'form-control email_personne'}),
                'nom' : forms.TextInput(attrs={'class': 'form-control nom_personne'}),
                'prenom' : forms.TextInput(attrs={'class':'form-control prenom_personne'}),
                'sexe' : forms.Select(attrs={'class':'form-control sexe_personne'}),
                'adresse' : forms.TextInput(attrs={'class':'form-control adresse_personne'}),
                'num_tel' : forms.TextInput(attrs={'class':'form-control num_tel_personne'}),
                'type' : forms.Select(attrs={'class':'form-control type_personne'}),
                'code_postal' : forms.TextInput(attrs={'class':'form-control postal_code_personne'}),
                
        }
        
    
        
class centreFormationForm(forms.ModelForm):
    
    username = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput) 

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']
    
    def save(self, commit=True):
        user = super(centreFormationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control mb-3 username_center', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3 email_center', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3 password_center', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control password2_center', 'placeholder': 'Repeat Password'})

    
    class Meta:      
        model = Centre_formation
        fields = ['username','password','email', 'nom_du_centre','responsable', 'type', 'code_postal']
        widgets = {
                'username' : forms.TextInput(attrs={'class': 'form-control username_center'}),
                'email' : forms.TextInput(attrs={'class':'form-control email_center'}),
                'password' : forms.PasswordInput(attrs={'class': 'form-control mb-3 password_personne'}),
                'nom_du_centre' : forms.TextInput(attrs={'class': 'form-control nom_center'}),
                'responsable' : forms.TextInput(attrs={'class':'form-control respo_center'}),
                'type' : forms.Select(attrs={'class':'form-control type_center'}),
                'code_postal' : forms.TextInput(attrs={'class':'form-control postal_code_center'})
        }

class ActiviteForm(ModelForm):
    class Meta:
        model = Activite
        fields = '__all__'
        exclude = ['membres']

class PartenaireForm(ModelForm):
    class Meta:
        model = Partenaire
        fields = '__all__'

class EtablissementForm(ModelForm):
    class Meta:
        model = Etablissement
        fields = '__all__'
        

class PasswordChangeCustomForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': "Votre ancien mot passe"})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "Votre nouveau mot passe"})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "Répétez votre nouveau mot de passe"})



class AdherantForm(ModelForm):
    class Meta:
        model = Adherent
        fields = ['id_membre', 'id_abonnement']

