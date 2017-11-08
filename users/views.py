# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db import connection
from schema.models import like_recipe, Recipes

@login_required
def get_user_home(request):
    cur = request.user
    context = {'user': cur}
    return render(request, "user_home.html", context)



def signup(request):
    if request.method == 'POST':
	form = UserCreationForm(request.POST)
	if form.is_valid():
	    form.save()
	   # username = form.cleaned_data.get('username')
	   # passwd = form.cleaned_data.get('password')
	   # user = authenticate(username=username, password=passwd)
	   # login(self.request, user)
	    return redirect('home')
    else:
	form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def get_my_recipes(request):
    username = request.user.username
    result = Recipes.objects.filter(creator = username)
    diction = {'usr':True,
               'table':result,
               'favorite':False}
    return render(request, 'user_recipes.html', diction)

def get_my_favorites(request):
    uid = request.user.id
    cursor = connection.cursor()
    cursor.callproc('sp_getUserFavorite', [uid,])
    result = cursor.fetchall()
    cursor.close()
    diction = {'usr':True,
               'table':result,
               'favorite':True
               }
    return render(request, 'user_recipes.html', diction)

def add_to_favorites(request):
    rid = request.POST.get('recipeID')
    recipe = Recipes.objects.get(rid = rid)
    like = like_recipe(user_id = request.user, r_id = recipe)
    like.save()
    return render(request, 'success.html')

def go_to_change_page(request):
    rname = request.POST.get('recipeName2')
    recipeID = request.POST.get('recipeID')
    return render(request, 'change_recipe.html', {'rname':rname, 'recipeID':recipeID})

def change_my_recipe(request):
    rid = request.POST.get('recipeID')
    name = request.POST.get('name')
    desc = request.POST.get('desc', '')
    cal = request.POST.get('calorie')
    pro = request.POST.get('protein')
    fat = request.POST.get('fat')
    sod = request.POST.get('sodium')
    cursor = connection.cursor()
    cursor.callproc('sp_updateRecipes',[rid, name, cal, pro, fat, sod,])
    cursor.close()
    return render(request, 'success.html')

def delete_recipe(request):
    recipeName = request.POST.get('recipeID')
    cursor = connection.cursor()
    cursor.callproc('sp_deleteRecipe', [recipeID, ])
    cursor.callproc('sp_deleteRecipeRelation', [recipeID, ])
    cursor.callproc('sp_deleteRecipeTag', [recipeID, ])
    cursor.close()
    return render(request, 'success.html')

def rate_recipe(request):
    rating = request.POST.get('rating-user')
    recipeID = request.POST.get('recipeID')
    cursor = connection.cursor()
    cursor.callproc('sp_updateRecipesRating', [recipeID, rating,])
    cursor.close()
    return render(request, 'success.html')
