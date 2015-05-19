# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aureva_core', '0011_auto_20150516_1950'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='track',
            options={'ordering': ['-date_uploaded']},
        ),
    ]
