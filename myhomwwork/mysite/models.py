from django.db import models
from datetime import datetime, timedelta
from django.urls import reverse
# Create your models here.
class Staff(models.Model):
    staff_id = models.AutoField('Id', primary_key=True, default=1)
    name = models.CharField("Name",max_length=20)
    department = models.CharField('Department',max_length=20)
    title = models.CharField('Position',max_length=100)
    gender = models.CharField('Gender',max_length=10)
    description = models.TextField()
    entry_time = models.DateTimeField('Created Time',default=datetime.now)
    salary = models.DecimalField('Salary',max_digits=10,decimal_places=2)
    updated_by=models.CharField(max_length=20,default='huziyu')
    updated_at = models.DateTimeField(auto_now=True)
    def get_absolute_url(self): 
        return reverse('book_list')
    
    def __str__(self):
        return self.title
