# Generated by Django 3.2.6 on 2021-08-29 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenform_app', '0003_alter_membre_image_profil'),
    ]

    operations = [
        migrations.AddField(
            model_name='abonnement',
            name='type_abonnement',
            field=models.CharField(choices=[('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Gold', 'Gold')], max_length=30, null=True),
        ),
    ]
