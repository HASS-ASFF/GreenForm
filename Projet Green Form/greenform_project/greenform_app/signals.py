
from .models import Centre_formation, Membre
from django.contrib.auth.models import Group, User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Membre)
def create_admin(sender, instance, created, **kwargs):
    if created and instance.is_superuser == False:
        user_group = Group.objects.get(id=3)
        instance.groups.add(user_group)
        
post_save.connect(create_admin, sender=Membre)
