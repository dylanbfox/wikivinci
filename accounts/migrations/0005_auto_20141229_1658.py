# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_cropping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(default=b'static/core/images/test_stock_img.png', upload_to=b'profile_pics'),
            preserve_default=True,
        ),
    ]
