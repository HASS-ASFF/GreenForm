# Generated by Django 3.2.6 on 2021-08-24 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenform_app', '0002_membre_image_profil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membre',
            name='image_profil',
            field=models.ImageField(blank=True, default='default_img.webp', null=True, upload_to='profil_photo/'),
        ),
    ]
