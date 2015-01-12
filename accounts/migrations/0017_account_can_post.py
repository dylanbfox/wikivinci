# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20150111_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='can_post',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
