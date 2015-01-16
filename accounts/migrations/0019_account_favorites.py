# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0019_auto_20150111_2220'),
        ('accounts', '0018_auto_20150111_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='favorites',
            field=models.ManyToManyField(to='posts.Post', null=True),
            preserve_default=True,
        ),
    ]
