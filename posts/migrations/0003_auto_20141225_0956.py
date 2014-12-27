# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_link_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='slug',
            field=models.CharField(unique=True, max_length=99),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='link',
            name='title',
            field=models.CharField(unique=True, max_length=200),
            preserve_default=True,
        ),
    ]
