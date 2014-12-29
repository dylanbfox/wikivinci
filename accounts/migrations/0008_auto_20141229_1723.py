# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20141229_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
