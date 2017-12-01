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
        	diff ++
    diff += len(tags2) - diff
    return diff

def recommend_engine(favorites, time_tag, user):
	diction = {}
	for recipe in favorites:
		tags = contain_tag.objects.filter(r_id = recipe)
		diction[recipe] = tags
	all_recipe = Recipes.objects.all()
	result_list = []
	for target in all_recipe:
		if target not in favorites:
			total = 0
			tags2 = contain_tag.objects.filter(r_id = target)
			for key, val in diction:
				total += cal_distance(val, tags2)
			result_list.append((total, target))
	sorted_list = sorted(result_list, key=lambda tup:tup[0])
	return sorted_list[:10]