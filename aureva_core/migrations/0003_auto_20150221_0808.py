# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aureva_core', '0002_auto_20150128_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=80)),
                ('desc', models.TextField(blank=True, default='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=300)),
                ('artists', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subgenre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=80)),
                ('desc', models.TextField(blank=True, default='')),
                ('genre', models.ForeignKey(to='aureva_core.Genre')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=300)),
                ('short_desc', models.CharField(blank=True, max_length=160, default='')),
                ('long_desc', models.TextField(blank=True, default='')),
                ('public', models.BooleanField(default=True)),
                ('tags', models.TextField(blank=True, default='')),
                ('genres', models.ManyToManyField(to='aureva_core.Subgenre')),
                ('release', models.ForeignKey(to='aureva_core.Release', blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='style',
            new_name='tagline',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='links',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, max_length=160, default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='tagline',
            field=models.CharField(default='', max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='biography',
            field=models.TextField(blank=True, default=''),
            preserve_default=True,
        ),
    ]
