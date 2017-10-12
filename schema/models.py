# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import uuid

# Create your models here.
#class User(models.Model):
#    ID = models.IntegerField(primary_key=True)
#    username = models.CharField(max_length=20)
#    email = models.EmalField()
#    password = models.CharField(max_length=50)
#    followers = models.ManyToManyField("self")
#    follower_num = models.IntegerField(default=0)

class Ingredient(models.Model):
    iid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    snack = models.BooleanField(default=False)
    vege = models.BooleanField(default=False)
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
    Creator = models.ForeignKey(User, default=None)

class Recipes(models.Model):
    rid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    vege = models.BooleanField(default=False)
    rating = models.DecimalField(decimal_places=3, max_digits=4)
    description = models.TextField()
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
    Creator = models.ForeignKey(User, default=None)

class Meals(models.Model):
    mid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=50)
    rating = models.DecimalField(decimal_places=3, max_digits=4)
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
    Creator = models.ForeignKey(User, default=None)

#class Mcontains(models.Model):
#    MID = models.IntegerField(primary_key=True)



#class Rcontains(models.Model):
#    RID = models.IntegerField(primary_key=True)
#    IIDS = models.ManyToManyField(Ingredient)
