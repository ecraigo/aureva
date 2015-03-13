# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aureva_core', '0003_auto_20150221_0808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subgenre',
            name='genre',
        ),
    ]
