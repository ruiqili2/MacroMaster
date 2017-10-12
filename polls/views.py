# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from schema.models import Recipes, Ingredient, Meals
from django.core.exceptions import *


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
        	#string = Recipes.objects.
       		rnames = Recipes.objects.filter(name = rname)
		if len(rnames) == 0:
			return HttpResponse("no such recipe")
        	html = ("<H1>%s</H1>", rnames)
           	 #html = ("<H1>%s</H1>", rname)
        	return HttpResponse(html)
        except Recipes.DoesNotExist:
            return HttpResponse("no such recipe")  
    else:
        return render(request, 'search.html')

def enter(request):
    return render(request, "add.html")
def ai(request):
    return render(request, "add_i.html")
def ar(request):
    return render(request, "add_r.html")
def am(request):
    return render(request, "add_m.html")

def pour(request):
    if request.method == 'POST':
        kind = request.POST.get('type')
        name = request.POST.get('name')
        desc = request.POST.get('desc', '')
        cal = request.POST.get('calorie')
        pro = request.POST.get('protein')
        fat = request.POST.get('fat')
        sod = request.POST.get('sodium')
        if kind == "ingredient":
            snack = request.POST.get('snack') == "T"
            vege = request.POST.get('vege') == "T"
            i = Ingredient(name = name,snack = snack,vege = vege,calories = cal,protein = pro,fat = fat,sodium = sod)
            i.save()
        if kind == "recipe":
            vege = request.POST.get('vege') == "T"
            r = Recipes(name = name, vege = vege, description = desc,calories = cal,protein = pro,fat = fat, sodium = sod)
            r.save()
        if kind == "meal":
            m = Meals(name = name, description = desc,calories = cal,protein = pro,fat = fat, sodium = sod)
            m.save()
        return HttpResponse("Success")  
    else:
        return render(request, 'add.html')

    return;