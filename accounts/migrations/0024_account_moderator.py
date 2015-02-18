# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20150216_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='moderator',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
