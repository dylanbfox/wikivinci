# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20150217_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='moderators',
            field=models.ManyToManyField(related_name='moderating_topics', null=True, to='accounts.Account', blank=True),
            preserve_default=True,
        ),
    ]
