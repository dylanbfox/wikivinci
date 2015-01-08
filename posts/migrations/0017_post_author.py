# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_account_can_comment'),
        ('posts', '0016_auto_20150101_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name='authored_posts', blank=True, to='accounts.Account', null=True),
            preserve_default=True,
        ),
    ]
