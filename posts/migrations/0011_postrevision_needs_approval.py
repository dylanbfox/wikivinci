# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20141228_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='postrevision',
            name='needs_approval',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
