from __future__ import unicode_literals
from schema.models import *
from django.shortcuts import render, redirect

def macro_recommend(cal, breakfast, lunch, dinner, break_table, lunch_table, dinner_table, request):
	if cal == 0.0:
		break_table += Recipes.objects.filter(calories = cal).order_by("rating")[:3]
		break_id = [b.rid for b in break_table]
		lunch_table += Recipes.objects.filter(calories = cal).order_by("rating").exclude(rid__in = break_id)[:3]
		lunch_id = [l.rid for l in lunch_table]
		dinner_table += Recipes.objects.filter(calories = cal).order_by("rating").exclude(rid__in = lunch_id)[:3]
		
	elif breakfast == 0.0 and lunch != 0.0 and dinner != 0.0:
		lunch_cal = cal * (lunch / (lunch + dinner))
		dinner_cal = cal - lunch_cal
		lunch_table += Recipes.objects.filter(calories__lte = lunch_cal + 5).filter(calories__gte = lunch_cal - 5).order_by("rating")[:10]
                lunch_id = [l.rid for l in lunch_table]
		dinner_table += Recipes.objects.filter(calories__lte = dinner_cal + 5).filter(calories__gte = dinner_cal - 5).exclude(rid__in = lunch_id).order_by("rating")[:10]

	elif lunch == 0.0 and breakfast != 0.0 and dinner != 0.0:
                break_cal = cal * (breakfast / (breakfast + dinner))
                dinner_cal = cal - break_cal
                break_table += Recipes.objects.filter(calories__lte = break_cal + 5).filter(calories__gte = break_cal - 5).order_by("rating")[:10]
                break_id = [b.rid for b in break_table]
                dinner_table += Recipes.objects.filter(calories__lte = dinner_cal + 5).filter(calories__gte = dinner_cal - 5).exclude(rid__in = break_id).order_by("rating")[:10]
	
	elif dinner == 0.0 and breakfast != 0.0 and lunch != 0.0:
                lunch_cal = cal * (lunch / (lunch + breakfast))
                break_cal = cal - lunch_cal
                lunch_table += Recipes.objects.filter(calories__lte = lunch_cal + 5).filter(calories__gte = lunch_cal - 5).order_by("rating")[:10]
                lunch_id = [l.rid for l in lunch_table]
		break_table += Recipes.objects.filter(calories__lte = break_cal + 5).filter(calories__gte = break_cal - 5).exclude(rid__in = lunch_id).order_by("rating")[:10]
	
	elif breakfast != 0.0 and lunch == 0.0 and dinner == 0.0:
                break_table += Recipes.objects.filter(calories__lte = cal + 5).filter(calories__gte = cal - 5).order_by("rating")[:10]
	
	elif lunch != 0.0 and breakfast == 0.0 and dinner == 0.0:
                lunch_table += Recipes.objects.filter(calories__lte = cal + 5).filter(calories__gte = cal - 5).order_by("rating")[:10]
	
	elif lunch == 0.0 and breakfast == 0.0 and dinner != 0.0:
                dinner_table += Recipes.objects.filter(calories__lte = cal + 5).filter(calories__gte = cal - 5).order_by("rating")[:10]
	
	else:
		#everything is filled in
		break_cal = cal * (breakfast / (breakfast + lunch + dinner))
		lunch_cal = cal * (lunch / (breakfast + lunch + dinner))
		dinner_cal = cal - lunch_cal - break_cal
		assert(dinner_cal >= 0)
		break_table += Recipes.objects.filter(calories__lte = break_cal + 5).filter(calories__gte = break_cal - 5).order_by("rating")[:10]
		break_id = [b.rid for b in break_table]
		lunch_table += Recipes.objects.filter(calories__lte = lunch_cal + 5).filter(calories__gte = lunch_cal - 5).exclude(rid__in = break_id).order_by("rating")[:10]
		lunch_id = [l.rid for l in lunch_table]
                dinner_table += Recipes.objects.filter(calories__lte = dinner_cal + 5).filter(calories__gte = dinner_cal - 5).exclude(rid__in = lunch_id)[:10]

