# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db import connection
from schema.models import like_recipe

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
    cursor = connection.cursor()
    cursor.callproc('get_my_recipes',[username,])
    result = cursor.fetchall()
    names = [item[1] for item in result]
    return render(request, 'user_recipes.html', {'names': names, "usr":True, "table":result, "favorite":False})

def get_my_favorites(request):
    username = request.user.username
    result = like_recipe.objects.filter(userName = username)
    print "in get_my_favorite"
    names = [item.recipeName for item in result]
    for thing in names:
        print thing
    return render(request, 'user_recipes.html', {'names': names, "usr":True, "table":result, "favorite":True})

def add_to_favorites(request):
    username = request.user.username
    recipeName = request.POST.get('recipeName')
    print 'add_to_favorite'
    print recipeName
    like = like_recipe(userName = username, recipeName = recipeName)
    like.save()
    return render(request, 'success.html')

def go_to_change_page(request):
    rname = request.POST.get('recipeName2')
    return render(request, 'change_recipe.html', {'rname':rname})

def change_my_recipe(request):
    userName = request.user.username
    recipeName = request.POST.get('recipe')
    name = request.POST.get('name')
    desc = request.POST.get('desc', '')
    cal = request.POST.get('calorie')
    pro = request.POST.get('protein')
    fat = request.POST.get('fat')
    sod = request.POST.get('sodium')
    cursor = connection.cursor()
    cursor.callproc('sp_updateRecipes',[recipeName, name, desc, cal, pro, fat, sod,])
    cursor.callproc('sp_updateLikeRecipeName', [recipeName, name,])
    return render(request, 'success.html')

def delete_recipe(request):
    recipeName = request.POST.get('recipeName2')
    cursor = connection.cursor()
    cursor.callproc('sp_deleteRecipe', [recipeName, ])
    cursor.callproc('sp_deleteRecipeRelation', [recipeName, ])
    return render(request, 'success.html')

def rate_recipe(request):
    rating = 0
    recipeName = ""
    cursor = connection.cursor()
    cursor.callproc('sp_updateRecipesRating', [recipeName, rating,])
    return render(request, 'success.html')
