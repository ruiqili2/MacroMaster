# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

@login_required
def get_user_home(request):
    context = {}
    return render(request, "user_home.html", context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = "signup.html"


