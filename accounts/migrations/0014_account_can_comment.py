# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20150105_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='can_comment',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
