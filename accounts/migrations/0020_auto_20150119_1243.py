# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_account_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='favorites',
            field=models.ManyToManyField(to='posts.Post', null=True, blank=True),
            preserve_default=True,
        ),
    ]
