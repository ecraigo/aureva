# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('aureva_core', '0009_auto_20150516_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='date_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 16, 19, 42, 51, 366319), auto_now_add=True),
            preserve_default=False,
        ),
    ]
