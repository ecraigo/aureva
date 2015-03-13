# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aureva_core', '0005_subgenre_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='')),
                ('rating', models.IntegerField(default=0)),
                ('track', models.ForeignKey(to='aureva_core.Track')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='track',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='track',
            name='file',
            field=models.FileField(null=True, upload_to='tracks'),
            preserve_default=True,
        ),
    ]
