from django.db import models

# Create your models here.
class People(models.Model):
    unique_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    age = models.IntegerField()
    
    def __str__(self):              # __unicode__ on Python 2
        return self.first_name +" "+ self.last_name

    