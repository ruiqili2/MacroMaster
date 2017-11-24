# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from schema.models import Recipes, Ingredient, Meals, like_recipe, Recipes_detail, Recipes_tag, contain_tag
from django.core.exceptions import *
from django.template.loader import render_to_string, get_template
from django_tables2 import RequestConfig
from django.db import connection
import django_tables2 as tables
import wikipedia

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

def return_success(request):
  return render(request, "success.html")


def get_list(request):
    if request.method == 'POST':
        rname = request.POST.get('recipe_name', None)
        in_table = Ingredient.objects.filter(name = rname)
       	re_table = Recipes.objects.filter(name__icontains = rname).order_by("rating")[:10]
	if len(re_table) + len(in_table) == 0:
            return HttpResponse("no such recipe nor ingredient")          
        return render(request, "user_recipes.html", {"in_table":in_table, "re_table":re_table, "usr":False})
    else:
        return render(request, 'search.html')

def get_list_tag(request):
    if request.method == 'POST':
        tname = request.POST.get('tag_name', None)
        tag_table = Recipes_tag.objects.filter(detail = tname)
	if len(tag_table) == 0:
		return HttpResponse("No such tag exist.")
	tid = tag_table[0].id
	con_table = contain_tag.objects.filter(t_id = tid)
	nl = [tag.r_id.name for tag in con_table]
        re_table = Recipes.objects.filter(name__in = nl).order_by("rating")[:10]
        in_table = Ingredient.objects.filter(name__in = nl)
	if len(re_table) + len(in_table) == 0:
            return HttpResponse("No other recipe found.")
        return render(request, "user_recipes.html", {"in_table":in_table, "re_table":re_table, "usr":False})
    else:
        return render(request, 'search.html')

def show_ingredient(request):
    return redirect("home.html")


def show_result(request):
    if request.method != 'POST':
    	return render(request, 'home.html')
    rname = request.POST.get('check')
    id = request.POST.get('recipeID')
    id = id.replace("-", "")
    already = request.POST.get('already')
    rec = Recipes.objects.get(rid=id)
    cal = rec.calories
    pro = rec.protein
    fat = rec.fat
    sod = rec.sodium
    creator = rec.creator
    rname = rec.name
    raw_rate = rec.rating
    carb = (cal - pro * 4.0 + fat * 9.0) / 4.0
    if carb < 0:
	carb = 0.0
# rating = str(raw_rate) + "%"
    rating_display = str(raw_rate) + ""
    rating = str(raw_rate*10) + "%"
    table = {"Calories":cal,
             "Protein":pro,
             "Fat":fat,
             "Sodium":sod,
	     "Carb": carb
    }
    cursor = connection.cursor()
    cursor.callproc("sp_getRecipeTags",[id, ])
    result = cursor.fetchall()
    tags = [item[1] for item in result]
    diction = {"myFavorites": False,
               "table":table,
               "name":rname,
               # "rating":rating,
               "rating": raw_rate,
               "creator":creator,
               "recipeID": id,
               "tags" : tags,
               "rating_display" : rating_display
    }
    f = like_recipe.objects.filter(user_id = request.user, r_id = rec)
    diction["myFavorites"] = len(f) != 0
    cursor.close()
    return render(request, "show_result.html", diction)  


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
        desc = request.POST.get('desc', '')
        cal = request.POST.get('calorie')
        pro = request.POST.get('protein')
        fat = request.POST.get('fat')
        sod = request.POST.get('sodium')
       	if kind == "add ingredient":
       	    i = Ingredient(name = name, calories = cal,protein = pro,fat = fat,sodium = sod, creator = username)
       	    i.save()
       	if kind == "add recipe":
            instructions = request.POST.get('message')
       	    r = Recipes(name = name,rating = 0,calories = cal,protein = pro,fat = fat, sodium = sod, creator = username)
       	    r.save()
            id = r.rid
            r_d = Recipes_detail(r_id = r, instructions= instructions)
            r_d.save()
       	if kind == "add meal":
       	    m = Meals(name = name,rating = 0, calories = cal,protein = pro,fat = fat, sodium = sod, creator = username)
       	    m.save()
       	return redirect("home.html")
    else:
        return render(request, 'add.html');


def check_recipe_ins(request):
    recipeName = request.POST.get('recipeName')
    recipeID= request.POST.get('recipeID')
    recipeID = recipeID.replace("-", "")
    try:
        detail = Recipes_detail.objects.get(r_id = recipeID)
        text = detail.instructions
	##text = text.replace('\n', '<br>')
	
    except Recipes_detail.DoesNotExist:
        text = "we don't know"
    diction = {
        'recipeName' : recipeName,
        'recipeID' : recipeID,
        'text' : text
    }
    return render(request, "recipe_instructions.html", diction)

def contact(request):
    return render(request, "contact.html")

def about(request):
    return render(request, "about.html")

