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

class MembreManager(BaseUserManager):
    """Helps Django work with our custom user model."""
    
    # def create_user(self, email, name, password=None):
    #     """Creates a user profile object."""

    #     if not email:
    #         raise ValueError('Users must have an email address.')

    #     email = self.normalize_email(email)
    #     user = self.model(email=email, username=name)

    #     user.user_id = -1
    #     user.set_password(password)
    #     user.save(using=self._db)

    #     return user
    
    # def create_superuser(self, email, username, password):
    #     """Creates and saves a new superuser with given details."""

    #     user = self.create_user(email = email, username = username, password = password)

    #     user.is_superuser = True

    #     user.save(using=self._db)
        
        ##################
        
    def create_superuser(self, username, password,email, **other_fields):    
        # other_fields.setdefault('is_staff', True)
        # other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)
    #  user = self.create_user(email = email, username = username, password = password)
        user = self.create_user(
        username=username,
        email=email,
        password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
        # user.user_id = -1
        # if other_fields.get('is_staff') is not True:
        #     raise ValueError(
        #         'Superuser must be assigned to is_staff=True.')
        # if other_fields.get('is_superuser') is not True:
        #     raise ValueError(
        #         'Superuser must be assigned to is_superuser=True.')

        # return self.create_user(username, email, password, **other_fields)
    # def save_user(self, username, email, password, **extra_fields):
    #     """
    #     Creates and saves a User with the given email and password.
    #     """
      
       
    def create_user(self,username, email=None, password=None, **other_fields):
        if not username:
            raise ValueError('The given username must be set')
        
        # other_fields['is_staff'] = False
        # username = self.get_by_natural_key(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,  **other_fields)
        # Call this method for password hashing
        user.set_password(password)
        user.save(using=self._db)
        return user
        # return self.save_user(username, email, password, **other_fields)

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
    
    # last_read = models.BooleanField(default=False)
    
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

    # @property
    # def is_superuser(self):        
    #     return self.is_superuser


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
    code_postal = models.CharField(blank=True, max_length=10, null=True)
    num_tel = models.CharField(max_length=30,blank=True)

    def __str__(self):
        return self.nom
    
    class Meta:
        db_table = 'Personne lambda'
    
    def save(self,*args,**kwargs):
        qrcode_img = qrcode.make("Information Membre:\n\n"+"Nom: "+self.nom+"\nPrenom: "+self.prenom+"\nSexe: "+self.sexe
        +"\nAdresse: "+self.adresse+"\nCode Postal: "+self.code_postal+"\nNumero de téléphone: "+self.num_tel
        +"\nType de membre: "+self.type)
        canvas = Image.new('RGB',(qrcode_img.pixel_size, qrcode_img.pixel_size),'white')
        # draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.nom}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname,File(buffer),save=False)
        canvas.close()
        super().save(*args, **kwargs)
    

class Centre_formation(Membre):
    
    nom_du_centre = models.CharField(max_length=30)
    code_postal = models.CharField(null=True, max_length=10)
    responsable = models.CharField(max_length=30)
    
    def save(self,*args,**kwargs):
        qrcode_img = qrcode.make("Information Membre:\n\n"+"Nom du centre: "+self.nom_du_centre+"\Responsable: "+self.responsable+"\Code Postal: "+self.code_postal
        +"\nType de membre: "+self.type)
        canvas = Image.new('RGB',(qrcode_img.pixel_size, qrcode_img.pixel_size),'white')
        # draw = ImageDraw.Draw(canvas)
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