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
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
    creator = models.CharField(max_length = 50, default = 'admin')

    def _str_(self):
        return self.name

    def get_id(self):
        return self.iid

class Recipes(models.Model):
    rid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    rating = models.DecimalField(decimal_places=3, max_digits=4)
    rating_num = models.IntegerField(default = 0)
    description = models.TextField()
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
    creator = models.CharField(max_length = 50, default = 'admin')

    def _str_(self):
        return self.name

    def get_id(self):
        return self.rid



class Meals(models.Model):
    mid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=50)
    rating = models.DecimalField(decimal_places=3, max_digits=4)
    rating_num = models.IntegerField(default = 0)
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    sodium = models.IntegerField()
    creator = models.CharField(max_length = 50, default = 'admin')

class like_recipe(models.Model):
    user_id = models.ForeignKey(null=True, User)
    r_id = models.ForeignKey(null=True, Recipes)

class Recipes_tag(models.Model):
    detail = models.CharField(max_length=50)

class contain_tag(models.Model):
    r_id = models.ForeignKey(null=True, Recipes)
    t_id = models.ForeignKey(null=True, Recipes_tag)


