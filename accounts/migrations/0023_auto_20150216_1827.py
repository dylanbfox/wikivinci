# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20150215_1732'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='fav_topics',
            new_name='fav_tags',
        ),
    ]
