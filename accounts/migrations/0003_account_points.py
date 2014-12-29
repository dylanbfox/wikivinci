# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141224_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='points',
            field=models.IntegerField(default=5),
            preserve_default=True,
        ),
    ]
