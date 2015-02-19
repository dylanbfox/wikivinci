# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0004_auto_20150218_1211'),
        ('accounts', '0024_account_moderator'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='subscribed_topics',
            field=models.ManyToManyField(related_name='subscribers', null=True, to='topics.Topic', blank=True),
            preserve_default=True,
        ),
    ]
