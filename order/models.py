from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=200)
    discription = models.TextField(null=True,blank=True)
    price = models.PositiveIntegerField()

