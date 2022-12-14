# Generated by Django 4.0.4 on 2022-09-28 18:58

import client.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_remove_folder_file_filefolder'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filefolder',
            name='file',
            field=models.FileField(upload_to=client.models.directory_folder_path),
        ),
    ]
