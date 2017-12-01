from schema.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
from models import UserProfile

def cal_distance(tags1, tags2):
    diff = 0
    for tag in tags1:
        if tag in tags2:
        	continue
        else:
        	diff += 1
    diff += len(tags2) - diff
    return diff

def recommend_engine(favorites_recipes, time_tag, user):
    diction = {}
    favorites = [fr.r_id for fr in favorites_recipes]
    for recipe in favorites:
	tags = contain_tag.objects.filter(r_id = recipe)
	diction[recipe] = tags
    print("...created tags dictionay...")
    all_recipe = Recipes.objects.all()
    result_list = []
    print("...fetched all recipe...")
    print(len(all_recipes))
    for target in all_recipe:
        if target not in favorites:
	    total = 0
	    tags2 = contain_tag.objects.filter(r_id = target)
	    for key, val in diction.items():
	        total += cal_distance(val, tags2)
		if total > 50:
		    break
	    if total > 50:
		continue
	    result_list.append((total, target))
    print("...finished calculation...")
    sorted_list = sorted(result_list, key=lambda tup:tup[0])
    print sorted_list[:10]
    return sorted_list[:10]
