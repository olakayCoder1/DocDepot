# Generated by Django 4.0.4 on 2022-09-27 16:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='shared_users',
            field=models.ManyToManyField(blank=True, null=True, related_name='allowed_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
