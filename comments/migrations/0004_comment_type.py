# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20141228_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='type',
            field=models.CharField(default=b'2', max_length=2, choices=[(b'1', b'comment'), (b'2', b'reply')]),
            preserve_default=True,
        ),
    ]
