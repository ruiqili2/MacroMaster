# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from schema.models import Recipes
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
       		rnames = [c.name for c in Recipes.objects.filter(name = rname)]
        	html = ("<H1>%s</H1>", rnames[0])
            #html = ("<H1>%s</H1>", rname)
        	return HttpResponse(html)
        except Recipes.DoesNotExist:
            return HttpResponse("no such recipe")  
    else:
        return render(request, 'search.html')
