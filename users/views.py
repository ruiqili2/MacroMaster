# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

@login_required
def get_user_home(request):
    context = {}
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
