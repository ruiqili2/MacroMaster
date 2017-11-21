# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db import connection
from schema.models import like_recipe, Recipes, Recipes_detail
from models import UserProfile

@login_required
def get_user_home(request):
    cur = request.user
    context = {'userName': cur}
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
    rid = rid.replace("-", "")
    recipe = Recipes.objects.get(rid = rid)
    like = like_recipe(user_id = request.user, r_id = recipe)
    like.save()
    return render(request, 'success.html')

def del_from_favorites(request):
    rid = request.POST.get('recipeID')
    rid = rid.replace("-", "")
    print rid
    recipe = Recipes.objects.get(rid = rid)
    like_recipe.objects.filter(user_id = request.user, r_id = recipe).delete()
    return render(request, 'success.html')

def go_to_change_page(request):
    rname = request.POST.get('recipeName2')
    recipeID = request.POST.get('recipeID')
    recipeID = recipeID.replace("-", "")
    recipe = Recipes.objects.get(rid = recipeID)
    instructions = Recipes_detail.objects.get(r_id = recipe)
    return render(request, 'change_recipe.html', {'rname':rname, 'recipeID':recipeID, 'recipe' : recipe, 'instructions':instructions.instructions})

def change_my_recipe(request):
    rid = request.POST.get('recipeID')
    rid = rid.replace("-", "")
    name = request.POST.get('name')
    desc = request.POST.get('desc', '')
    cal = request.POST.get('calorie')
    pro = request.POST.get('protein')
    fat = request.POST.get('fat')
    sod = request.POST.get('sodium')
    instructions = request.POST.get('message')
    cursor = connection.cursor()
    cursor.callproc('sp_updateRecipes',[rid, name, cal, pro, fat, sod,])
    cursor.callproc('sp_updateRecipeDetail', [rid, instructions,])
    cursor.close()
    return render(request, 'success.html')

def delete_recipe(request):
    recipeID= request.POST.get('recipeID')
    recipeID = recipeID.replace("-", "")
    cursor = connection.cursor()
    cursor.callproc('sp_deleteRecipeRelation', [recipeID, ])
    cursor.callproc('sp_deleteRecipeTag', [recipeID, ])
    cursor.callproc('sp_deleteRecipeDetail', [recipeID, ])
    cursor.callproc('sp_deleteRecipe', [recipeID, ])
    cursor.close()
    return render(request, 'success.html')

def rate_recipe(request):
    rating = request.POST.get('rating-user')
    recipeID = request.POST.get('recipeID')
    recipeID = recipeID.replace("-", "")
    cursor = connection.cursor()
    cursor.callproc('sp_updateRecipesRating', [recipeID, rating,])
    cursor.close()
    return render(request, 'success.html')

def go_to_change_profile(request):
    return render(request, 'change_profile.html')

def edit_profile(request):
    newPhoto = request.FILES.get("file")
    newBio = request.POST.get("bio")
    user = request.user
    u, created = UserProfile.objects.get_or_create(user = user)
    u.avatar = newPhoto
    u.bio = newBio
    u.save()
    return render(request, 'success.html')




