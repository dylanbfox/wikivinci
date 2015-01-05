# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_account_twitter_handle'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fav_topics',
            field=models.CharField(max_length=999, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(default=b'profile_pics/default_profile_pic.jpg', upload_to=b'profile_pics'),
            preserve_default=True,
        ),
    ]
