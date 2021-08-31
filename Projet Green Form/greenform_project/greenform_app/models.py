from django.db import models
from django.contrib.auth.models import AbstractUser, User
import qrcode
from io import BytesIO
from PIL import Image,ImageDraw
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,UserManager


sexe = (
    ("H","Homme"),
    ("F","Femme"),
)

type_membre = (
    ("Bénévole","Bénévole"),
    ("Donateur","Donateur"),
    ("Autre","Autre"),
)

type_abonnement = (
    ("Bronze", "Bronze"),
    ("Silver", "Silver"),
    ("Gold", "Gold"),
)

class MembreManager(BaseUserManager):
     
    def create_superuser(self, username, password,email, **other_fields):    
        user = self.create_user(
        username=username,
        email=email,
        password=password,
        is_superuser = True,
        is_staff = True,
        )
        # user.is_superuser = True
        # user.is_staff = True
        user.save(using=self._db)
        return user
    
    def create_user(self,username, email=None, password=None, **other_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,  **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
class Membre(AbstractUser,PermissionsMixin):

    username_validator = UnicodeUsernameValidator()
    first_name = None
    last_name = None
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        null=True
    )
    password = models.CharField(_('password'), max_length=128, null=True)
    type = models.CharField(max_length=30,choices=type_membre, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/',blank=True)
    image_profil = models.ImageField(null=True, default="default_img.webp",upload_to='profil_photo/', blank=True )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    
    USERNAME_FIELD = 'username'
    
    objects = MembreManager()
    
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'Membres'
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def get_photo_url(self):
        if self.image_profil and hasattr(self.image_profil, 'url'):
            return self.image_profil.url
        else:
            return "/static/img/default_img.webp"


class Abonnement(models.Model):
    type_abonnement = models.CharField(max_length=30,choices=type_abonnement, null=True)
    
    def __str__(self):
        return self.type_abonnement

class Adherent(models.Model):
    id_membre = models.ForeignKey(Membre,on_delete=models.CASCADE)
    date_abonnement = models.DateTimeField(auto_now_add=True, blank=True)
    id_abonnement = models.ForeignKey(Abonnement,on_delete=models.CASCADE)

    class Meta:
        db_table = 'Adhérant'
        
    # def __str__(self):
    #     return ''

class Personne(Membre):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    sexe = models.CharField(max_length=30, choices=sexe)
    adresse = models.CharField(max_length=100,blank=True)
    code_postal = models.CharField(blank=True, max_length=10, null=True)
    num_tel = models.CharField(max_length=30,blank=True)

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
    code_postal = models.CharField(blank=True, max_length=10, null=True)
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


    def __str__(self):
        
        return self.nom_du_centre

    class Meta:
        db_table = 'Centre de formation'



class Partenaire(models.Model):
    nom = models.CharField(max_length=30)
    adresse = models.CharField(max_length=100)
    code_postal = models.CharField(blank=True, max_length=10, null=True)
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
    code_postal = models.CharField(blank=True, max_length=10, null=True)
    type_etablissement = models.CharField(max_length=30,choices=type_etab)
    representant = models.CharField(max_length=30)

    def __str__(self):
        return self.nom

class Activite(models.Model):
    nom = models.CharField(max_length=30)
    desc = models.CharField(max_length=100)
    membres = models.ManyToManyField(Membre,related_name='Participation',blank=True)
    id_partenaire = models.ForeignKey(Partenaire,on_delete=models.CASCADE)
    id_etablissement = models.ForeignKey(Etablissement,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.nom
