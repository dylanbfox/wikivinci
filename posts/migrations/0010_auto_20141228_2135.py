# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20141228_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postrevision',
            name='approver',
            field=models.ForeignKey(related_name='approved_post_revisions', blank=True, to='accounts.Account', null=True),
            preserve_default=True,
        ),
    ]
