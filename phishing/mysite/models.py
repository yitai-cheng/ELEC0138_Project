from django.db import models
from datetime import datetime, timedelta
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Staff(models.Model):
    staff_id = models.AutoField('Id', primary_key=True)
    name = models.CharField("Name",max_length=20)
    department = models.CharField('Department',max_length=20)
    title = models.CharField('Position',max_length=100)
    gender = models.CharField('Gender',max_length=10)
    description = models.TextField()
    entry_time = models.DateTimeField('Created Time',default=datetime.now)
    salary = models.DecimalField('Salary',max_digits=10,decimal_places=2)
    updated_by=models.CharField(max_length=20,default='huziyu')
    updated_at = models.DateTimeField(auto_now=True)
    email = models.EmailField('Email',max_length=100,default='example@example.com')
    def get_absolute_url(self): 
        return reverse('staff_list')
    
    def __str__(self):
        return self.title

class LoginCredential(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
class User(AbstractUser):
    password = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name="%(app_label)s_%(class)s_groups")
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name="%(app_label)s_%(class)s_user_permissions")
    email = models.EmailField(_('email address'), blank=True, null=True)