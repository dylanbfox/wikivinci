# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0021_post_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='topics',
            field=models.ManyToManyField(related_name='posts', null=True, to='topics.Topic', blank=True),
            preserve_default=True,
        ),
    ]
