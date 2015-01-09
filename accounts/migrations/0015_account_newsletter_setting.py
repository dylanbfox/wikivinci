# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_account_can_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='newsletter_setting',
            field=models.CharField(default=b'DAILY', max_length=50, choices=[(b'DAILY', b'daily'), (b'WEEKLY', b'weekly'), (b'NONE', b'none')]),
            preserve_default=True,
        ),
    ]
