# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20150119_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='twitter_oauth_secret',
            field=models.CharField(max_length=199, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='twitter_oauth_token',
            field=models.CharField(max_length=199, null=True, blank=True),
            preserve_default=True,
        ),
    ]
