# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20150119_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='newsletter_setting',
            field=models.CharField(default=b'DAILY', max_length=50, choices=[(b'DAILY', b'Daily'), (b'WEEKLY', b'Weekly'), (b'NONE', b"Never. I'm too smart already.")]),
            preserve_default=True,
        ),
    ]
