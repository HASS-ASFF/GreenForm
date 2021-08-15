from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from PIL import Image,ImageDraw
from django.core.files import File


sexe = (
    ("H","Homme"),
    ("F","Femme"),
)

type_membre = (
    ("Bénévole","Bénévole"),
    ("Donateur","Donateur"),
    ("Autre","Autre"),
)

class Membre(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes/',blank=True)
    
    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'Membres'

    

class Inscription(models.Model):
    id_membre = models.ForeignKey(Membre,on_delete=models.CASCADE)

    def __str__(self):
        return self.id_membre

class Abonnement(models.Model):
    numero = models.CharField(max_length=30)

    def __str__(self):
        return self.numero

class Adherent(models.Model):
    id_inscription = models.ForeignKey(Inscription,on_delete=models.CASCADE)
    date_abonnement = models.DateField()
    id_abonnement = models.ForeignKey(Abonnement,on_delete=models.CASCADE)

    def __str__(self):
        return self.id_abonnement

    class Meta:
        db_table = 'Adhérant'

class Personne(Membre):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    sexe = models.CharField(max_length=30, choices=sexe)
    adresse = models.CharField(max_length=100,blank=True)
    code_postal = models.IntegerField(null=True)
    num_tel = models.CharField(max_length=30,blank=True)
    type = models.CharField(max_length=30,choices=type_membre)

    def __str__(self):
        return self.nom

    class Meta:
        db_table = 'Personne lambda'
    
    def save(self,*args,**kwargs):
        qrcode_img = qrcode.make("Membre Forma-Green:\n\n"+"Nom: "+self.nom+"\nPrenom: "+self.prenom+"\nSexe: "+self.sexe
        +"\nAdresse: "+self.adresse+"\nCode Postal: "+str(self.code_postal)+"\nNumero de téléphone: "+self.num_tel
        +"\nType de membre: "+self.type)
        canvas = Image.new('RGB',(qrcode_img.pixel_size, qrcode_img.pixel_size),'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.nom}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        canvas.close()
        super().save(*args, **kwargs)

class Centre_formation(Membre):
    nom_du_centre = models.CharField(max_length=30)
    code_postal = models.IntegerField(null=True)
    responsable = models.CharField(max_length=30)

    def __str__(self):
        return self.nom_du_centre

    class Meta:
        db_table = 'Centre de formation'

    def save(self,*args,**kwargs):
        qrcode_img = qrcode.make("Membre Forma-Green:\n\n"+"Nom du centre: "+self.nom_du_centre+"\nResponsable: "+self.responsable+"\nCode postal: "+str(self.code_postal))
        canvas = Image.new('RGB',(qrcode_img.pixel_size, qrcode_img.pixel_size),'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.nom_du_centre}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        canvas.close()
        super().save(*args, **kwargs)



class Partenaire(models.Model):
    nom = models.CharField(max_length=30)
    adresse = models.CharField(max_length=100)
    code_postal = models.IntegerField()
    num_tel = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

type_etab = (
    ("Ecole","Ecole"),
    ("Université","Université"),
    ("Ecole de formation","Ecole de formation"),
    ("Centre","Centre"),
)
class Etablissement(models.Model):
    nom = models.CharField(max_length=30)
    adresse = models.CharField(max_length=100)
    code_postal = models.IntegerField()
    type_etablissement = models.CharField(max_length=30,choices=type_etab)
    representant = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class Activite(models.Model):
    nom = models.CharField(max_length=30)
    desc = models.CharField(max_length=100)
    membres = models.ManyToManyField(Membre,related_name='Participation')
    id_partenaire = models.ForeignKey(Partenaire,on_delete=models.CASCADE)
    id_etablissement = models.ForeignKey(Etablissement,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.nom