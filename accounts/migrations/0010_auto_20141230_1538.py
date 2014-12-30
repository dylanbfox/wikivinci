# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20141229_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='title',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='points',
            field=models.IntegerField(default=50),
            preserve_default=True,
        ),
    ]
