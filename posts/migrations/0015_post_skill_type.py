# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0014_auto_20141230_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='skill_type',
            field=models.CharField(default='BEGINNER', max_length=12, choices=[(b'BEGINNER', b'Beginner'), (b'INTERMEDIATE', b'Intermediate'), (b'ADVANCED', b'Advanced')]),
            preserve_default=False,
        ),
    ]
