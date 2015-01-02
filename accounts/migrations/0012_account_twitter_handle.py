# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20150101_2352'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='twitter_handle',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
