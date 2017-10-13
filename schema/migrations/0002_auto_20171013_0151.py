# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='Creator',
        ),
        migrations.RemoveField(
            model_name='meals',
            name='Creator',
        ),
        migrations.RemoveField(
            model_name='recipes',
            name='Creator',
        ),
    ]
