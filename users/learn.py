from schema.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
from models import UserProfile

def cal_distance(tags1, tags2, diction):
    diff = 0
    factor = 1
    for tag in tags1:
        if tag in tags2:
            factor = factor * diction[tag]
            continue
        else:
            diff += 1
    if len(tags2) > (len(tags1) - diff):
        diff += len(tags2) - len(tags1) + diff
    return diff * 1.0 / factor



def recommend_engine(favorites_recipes, time_tag, user):
    diction = {}
    w_diction = {}
    favorites = [fr.r_id for fr in favorites_recipes]
    big_list = []
    for recipe in favorites:
        ct = contain_tag.objects.filter(r_id = recipe)
        tag_list = list(set([t.t_id for t in ct]))
        diction[recipe] = tag_list
        for tag in tag_list:
            big_list.append(tag)
            if not tag in w_diction:
                w_diction[tag] = 1
            else:
                w_diction[tag] += 1
    print("...created tags dictionary...")
    all_recipe = Recipes.objects.all()
    result_list = []
    print("...fetched all recipe...")
    for target in all_recipe:
        if target not in favorites:
            if target.creator == user.username:
                continue
            total = 0
            ct = contain_tag.objects.filter(r_id = target)
            tags2 = list(set([t.t_id for t in ct]))
            if len(tags2) == 0:
                continue
            for key, val in diction.items():
                total += cal_distance(val, tags2, w_diction)
                    #if total > 50:
                    #break
                    #if total > 50:
#continue
        result_list.append((total, target))
    print("...finished calculation...")
    sorted_list = sorted(result_list, key=lambda tup:tup[0])
    print sorted_list[:10]
    return sorted_list[:10]
