# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import aureva_core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aureva_core', '0007_auto_20150402_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='waveform',
            field=models.ImageField(null=True, blank=True, upload_to='waveforms'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='track',
            name='file',
            field=aureva_core.fields.AudioField(null=True, upload_to='tracks', help_text='Must be in mp3, FLAC, wav, ogg, AAC, WebM, or mp4 formats. Files up to 100 MB are allowed.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='links',
            field=models.TextField(default='', blank=True, help_text='A place to show off your spaces on other websites. Up to 7 links permitted.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='thumb_large',
            field=models.ImageField(null=True, blank=True, upload_to='profile_images'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='thumb_small',
            field=models.ImageField(null=True, blank=True, upload_to='profile_images'),
            preserve_default=True,
        ),
    ]
