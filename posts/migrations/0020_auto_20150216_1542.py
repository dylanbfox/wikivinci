# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_auto_20150111_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='youtube_embed_url',
            field=models.CharField(default='', max_length=500, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='youtube_video',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
