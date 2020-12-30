from django.db import models

# Create your models here.
class Student(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    collegeid = models.EmailField()
    photo = models.ImageField(upload_to = 'images')
    password1 = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30) 