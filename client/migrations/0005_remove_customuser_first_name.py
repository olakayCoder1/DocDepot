# Generated by Django 4.0.4 on 2022-09-27 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_rename_user_name_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
    ]