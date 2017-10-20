# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from schema.models import Recipes, Ingredient, Meals
from django.core.exceptions import *
from django.template.loader import render_to_string, get_template
from django_tables2 import RequestConfig
import django_tables2 as tables

class RecipeTable(tables.Table):
    class Meta:
        model =  Recipes

class IngreTable(tables.Table):
    class Meta:
        model =  Ingredient

class MealTable(tables.Table):
    class Meta:
        model =  Meals


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    return render(request, "home.html")

def login(request):
	return render(request, "login.html")

def search_page(request):
## search recipes based on name
	return render(request, "search.html")

def search(request):
    if request.method == 'POST':
        rname = request.POST.get('recipe_name', None)
        try:
       	    rnames = Recipes.objects.filter(name = rname)
	    print rname
		# table = RecipeTable(rnames)
            if len(rnames) == 0:
                return HttpResponse("no such recipe")           
            return render(request, "show_result.html", {"results":rnames,"name":rname})
        except Recipes.DoesNotExist:
            return HttpResponse("no such recipe")
    elif request.method == 'GET':
	rname = request.GET.get('check', None)
        rnames = Recipes.objects.filter(name = rname)
	return render(request, "show_result.html", {"results":rnames})
    else:
        return render(request, 'search.html')

def enter(request):
    return render(request, "add.html")
def ai(request):
    return render(request, "add_i.html")
def aj(request):
    return render(request, "add_r.html")
def am(request):
    return render(request, "add_m.html")

def pour(request):
    if request.method == 'POST':
	username = request.user.username
        kind = request.POST.get('type')
        name = request.POST.get('name')
        esc = request.POST.get('desc', '')
        cal = request.POST.get('calorie')
        pro = request.POST.get('protein')
        fat = request.POST.get('fat')
        sod = request.POST.get('sodium')
       	if kind == "add ingredient":
       	    snack = request.POST.get('snack') == "T"
       	    vege = request.POST.get('vege') == "T"
       	    i = Ingredient(name = name,snack = snack,vege = vege,calories = cal,protein = pro,fat = fat,sodium = sod, creator = username)
       	    i.save()
       	if kind == "add recipe":
       	    vege = request.POST.get('vege') == "T"
       	    r = Recipes(name = name, vege = vege, description = desc,rating = 0,calories = cal,protein = pro,fat = fat, sodium = sod, creator = username)
       	    r.save()
       	if kind == "add meal":
       	    m = Meals(name = name, description = desc,rating = 0, calories = cal,protein = pro,fat = fat, sodium = sod, creator = username)
       	    m.save()
       	return redirect("home.html")
    else:
        return render(request, 'add.html');
