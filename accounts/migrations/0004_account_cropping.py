# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField(b'profile_pic', '250x250', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping'),
            preserve_default=True,
        ),
    ]
