# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import django_tables2 as tables

class SimpleTable(tables.Table):
    class Meta:
        model = Simple 