# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_postrevision'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='flagged',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='postrevision',
            name='post',
            field=models.ForeignKey(related_name='revisions', default=1, to='posts.Post'),
            preserve_default=False,
        ),
    ]
