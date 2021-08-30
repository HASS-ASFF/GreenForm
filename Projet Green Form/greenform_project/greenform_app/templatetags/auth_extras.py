import datetime
from django import template
from greenform_app.models import Adherent

register = template.Library()

@register.simple_tag()
def addDays(membre, days, i ):
   adherent = Adherent.objects.filter(id_membre = membre)
   validite = adherent[i].date_abonnement + datetime.timedelta(days=days)
   return validite.strftime("%Y-%m-%d %H:%M, %p")