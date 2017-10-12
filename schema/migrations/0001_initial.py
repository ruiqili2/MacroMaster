# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('iid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('snack', models.BooleanField(default=False)),
                ('vege', models.BooleanField(default=False)),
                ('calories', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('fat', models.IntegerField()),
                ('sodium', models.IntegerField()),
                ('Creator', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('mid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('text', models.CharField(max_length=50)),
                ('rating', models.DecimalField(max_digits=4, decimal_places=3)),
                ('calories', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('fat', models.IntegerField()),
                ('sodium', models.IntegerField()),
                ('Creator', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('rid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('vege', models.BooleanField(default=False)),
                ('rating', models.DecimalField(max_digits=4, decimal_places=3)),
                ('description', models.TextField()),
                ('calories', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('fat', models.IntegerField()),
                ('sodium', models.IntegerField()),
                ('Creator', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
