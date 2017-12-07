# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db import connection
from schema.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
from models import UserProfile
from learn import recommend_engine

@login_required
def get_user_home(request):
    cur = request.user
    try:
        img = request.user.profile.avatar
    except ObjectDoesNotExist:
        pf = UserProfile(user = cur)
        pf.save()
    return render(request, "user_home.html")

def signup(request):
    if request.method == 'POST':
	form = UserCreationForm(request.POST)
	if form.is_valid():
	    form.save()
        #username = form.cleaned_data.get('username')
        #passwd = form.cleaned_data.get('password')
        #user = authenticate(username=username, password=passwd)
        #pf = UserProfile(user = user)
        #pf.save()
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
    result = contain_tag.objects.filter(r_id = recipe)
    old_tags = [item.t_id.detail for item in result]
    new_tags = Recipes_tag.objects.all()

    return render(request, 'change_recipe.html', {'rname':rname, 'recipeID':recipeID, 'recipe' : recipe, 'instructions':instructions.instructions, 'old_tags': old_tags, 'new_tags': new_tags})

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
    tag_id = request.POST.getlist('tag_id[]')
    print "\n\n\nchange to ->: ", tag_id, "\n\n\n"
    cursor = connection.cursor()
    cursor.callproc('sp_updateRecipes',[rid, name, cal, pro, fat, sod,])
    cursor.callproc('sp_updateRecipeDetail', [rid, instructions,])
    # delete old recipe-tag tuple
    #cursor.callproc('sp_deleteContainTag', [rid,])
    # add new recipe-tag tuple
    '''for t_id in tag_id:
	tid = int(t_id)
	cursor.callproc('sp_insertContainTag', [rid, tid,])
    '''
    cursor.close()

    contain_tag.objects.filter(r_id = rid).delete()
    r = Recipes.objects.filter(rid = rid)[0]
    t_table = Recipes_tag.objects.filter(id__in = tag_id)
    for t in t_table:
	print "t:", t.detail
        new_t = contain_tag(r_id = r, t_id = t)
        new_t.save()
 
    
    return render(request, 'success.html')

def delete_recipe(request):
    recipeID= request.POST.get('recipeID')
    recipeID = recipeID.replace("-", "")
    Recipes_HitCount.objects.filter(recipe = recipeID).delete()
    Recipes_Comment.objects.filter(recipe = recipeID).delete()
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
    newPhoto = request.FILES.get("photo")
    newBio = request.POST.get("bio")
    user = request.user
    u, created = UserProfile.objects.get_or_create(user = user)
    if newPhoto:
        u.avatar = newPhoto
    u.bio = newBio
    u.save()
    return render(request, 'success.html')

def comment(request):
    user = request.user
    comment_txt = request.POST.get("comment_txt")
    rating = request.POST.get("rating-user")
    recipeID = request.POST.get("recipeID")
    recipeID = recipeID.replace("-", "")
    cursor = connection.cursor()
    cursor.callproc('sp_updateRecipesRating', [recipeID, rating,])
    cursor.close()
    recipe = Recipes.objects.get(rid = recipeID)
    new_comment = Recipes_Comment(user = user, recipe = recipe, rating = rating, comment = comment_txt)
    new_comment.save()
    return render(request, 'success.html')


def recommend(request):
## first check how many favorites.
    if request.method == 'GET':
        return
    hour = datetime.datetime.now().hour
    time_tag = None
    if 6 <= hour and hour <= 9:
        time_tag = "breakfast"
    elif 10 <= hour and hour <= 13:
        time_tag = "lunch"
    elif 14 <= hour and hour <= 20:
        time_tag = "dinner"
    user = request.user
    favorites = like_recipe.objects.filter(user_id = user)
    if len(favorites) < 10:
        error_message = "Sorry, we need at least 10 favorite recipes"
        return render(request, 'error.html', {"error_message": error_message})
    print("enter recommend")
    result = recommend_engine(favorites, time_tag, request.user)
    recommended = [r[1] for r in result]
    print [r.name for r in recommended]
    diction = {'usr':False,
               're_table':recommended,
               'favorite':False
               }
    return render(request, 'user_recipes.html', diction)




