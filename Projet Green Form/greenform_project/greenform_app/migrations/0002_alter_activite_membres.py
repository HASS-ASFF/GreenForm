# Generated by Django 3.2.6 on 2021-08-30 23:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenform_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activite',
            name='membres',
            field=models.ManyToManyField(blank=True, related_name='Participation', to=settings.AUTH_USER_MODEL),
        ),
    ]
