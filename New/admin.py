# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Ingredient, Recipes

admin.site.register(Ingredient)
admin.site.register(Recipes)

# Register your models here.
