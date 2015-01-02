# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20141230_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='title',
            field=models.CharField(max_length=59, null=True, blank=True),
            preserve_default=True,
        ),
    ]
