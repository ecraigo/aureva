# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('aureva_core', '0010_track_date_uploaded'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='track',
            options={'ordering': ['date_uploaded']},
        ),
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 5, 16, 19, 50, 11, 233759)),
            preserve_default=False,
        ),
    ]
