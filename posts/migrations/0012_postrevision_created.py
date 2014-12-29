# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_postrevision_needs_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='postrevision',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 28, 21, 46, 31, 497000), auto_now_add=True),
            preserve_default=False,
        ),
    ]
