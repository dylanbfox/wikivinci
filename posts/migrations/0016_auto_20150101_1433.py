# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_post_skill_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='skill_type',
            new_name='skill_level',
        ),
    ]
