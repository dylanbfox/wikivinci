# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_account_can_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='can_post',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
