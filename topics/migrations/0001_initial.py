# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20150216_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to=b'topic_imgs')),
                ('moderators', models.ManyToManyField(related_name='moderating_topics', to='accounts.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
