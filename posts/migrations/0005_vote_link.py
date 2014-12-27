# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20141227_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='link',
            field=models.ForeignKey(related_name='votes', default=1, to='posts.Link'),
            preserve_default=False,
        ),
    ]
