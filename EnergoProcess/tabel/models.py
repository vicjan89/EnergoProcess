from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=40)
    position = models.CharField(max_length=40)
    electrical_safety_group = models.CharField(max_length=3)
