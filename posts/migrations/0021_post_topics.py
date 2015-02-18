# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_auto_20150217_1419'),
        ('posts', '0020_auto_20150216_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='topics',
            field=models.ManyToManyField(related_name='posts', to='topics.Topic'),
            preserve_default=True,
        ),
    ]
