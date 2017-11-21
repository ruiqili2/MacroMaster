# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user   = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = 'static/pictures/UserPhoto/', default = 'static/pictures/UserPhoto/default-user.png')
    bio = models.TextField(default='', blank=True)

    def __str__(self):
        return 'Profile of {}'.format(self.user.username)

