# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aureva_core', '0006_auto_20150305_2217'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewRating',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('vote', models.BooleanField(default=True)),
                ('review', models.ForeignKey(to='aureva_core.Review')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='track',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='thumb_large',
            field=models.ImageField(upload_to='profile_images', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='thumb_small',
            field=models.ImageField(upload_to='profile_images', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='long_desc',
            field=models.TextField(blank=True, help_text='More track info.', verbose_name='Long description', default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='public',
            field=models.BooleanField(help_text='Privacy settings. A track that is public is visible from your profile, while a private track can only be seen by those with the link.', default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='short_desc',
            field=models.CharField(blank=True, max_length=160, help_text='A quick overview of your track. Up to 160 characters permitted.', verbose_name='Short description', default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(max_length=300, help_text='Up to 300 characters.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='biography',
            field=models.TextField(help_text='A place for you to explain a bit more about yourself.', default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='links',
            field=models.TextField(blank=True, help_text='A place to show off your spaces on other websites. Up to 8 links permitted.', default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='profile_images', help_text='Must be in .jpg, .png, or .gif formats. Files up to 4 MB are allowed.', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tagline',
            field=models.CharField(max_length=160, help_text='A short summary of who you are and what you do. Up to 160 characters permitted.', default=''),
            preserve_default=True,
        ),
    ]
