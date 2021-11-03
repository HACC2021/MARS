from django.db import models


# Create your models here.

class formdata(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=10)
    date = models.CharField(max_length=10)
    island = models.CharField(max_length=100)
    longitude = models.DecimalField(decimal_places=10, max_digits=1000000000)
    latitude = models.DecimalField(decimal_places=10, max_digits=100000000)
    identifying_characteristics = models.CharField(max_length=100)
    animal_behavior = models.CharField(max_length=100)
    number_of_beach_goers = models.IntegerField()
    picture = models.FileField(upload_to=None)





