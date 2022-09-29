from datetime import datetime
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        return self.create_user(email, username, password, **other_fields)


    def create_user(self, email, username,password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


def upload_to(instance, filename):
    return 'profiles/{filename}'.format(filename=filename)


def directory_path(instance, filename):
    return 'profiles/{0}/{1}'.format(instance.user.id ,filename) 


def directory_folder_path(instance, filename):
    return 'profiles/{0}/{1}'.format(instance.folder.user.id ,filename) 


class Folder(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True , blank=True)


    def __str__(self) -> str:
        return '{} , {}'.format(self.name , self.user.username)

    @property
    def files(self):
        print(FileFolder.objects.filter( folder__id=self.id))
        return FileFolder.objects.filter( folder__id=self.id)




class FileFolder(models.Model):
    file = models.FileField(upload_to=directory_folder_path)
    name = models.CharField(max_length=1000 , blank=True , null=True)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    shared_users = models.ManyToManyField(CustomUser, related_name='allowed_file_users' , null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True) 


class File(models.Model):
    file = models.FileField(upload_to=directory_path)
    name = models.CharField(max_length=1000 , blank=True , null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shared_users = models.ManyToManyField(CustomUser, related_name='allowed_users' , null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True) 

    def get_allowed_users(self):
        return File.objects.filter(id=self.id)


class Document(models.Model):
    file = models.FileField(upload_to=directory_path)

class TokenActivation(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)
    time = models.DateTimeField()
    email = models.EmailField()