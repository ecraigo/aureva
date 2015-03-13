# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aureva_core', '0004_remove_subgenre_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='subgenre',
            name='genre',
            field=models.ManyToManyField(to='aureva_core.Genre'),
            preserve_default=True,
        ),
    ]
