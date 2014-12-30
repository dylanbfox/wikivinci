# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20141229_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='downvoters',
            field=models.ManyToManyField(related_name='downvoted_posts', to='accounts.Account', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='upvoters',
            field=models.ManyToManyField(related_name='upvoted_posts', to='accounts.Account', blank=True),
            preserve_default=True,
        ),
    ]
