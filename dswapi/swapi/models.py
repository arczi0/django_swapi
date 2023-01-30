import django.utils.timezone
from django.db import models

# Create your models here.

class DataSet(models.Model):
    filename = models.CharField(max_length=255)
    downloaded_time = models.DateTimeField(auto_now_add=True)

class Character(models.Model):
    name = models.CharField(max_length=250)
    height = models.CharField(max_length=250)
    mass = models.CharField(max_length=250)
    hair_color = models.CharField(max_length=250)
    skin_color = models.CharField(max_length=250)
    eye_color = models.CharField(max_length=250)
    birth_year = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    homeworld = models.CharField(max_length=250)
    edited = models.CharField(max_length=250, default=' ')

