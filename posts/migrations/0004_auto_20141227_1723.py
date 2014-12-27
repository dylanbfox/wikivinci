# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141224_1938'),
        ('posts', '0003_auto_20141225_0956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.CharField(max_length=12, choices=[(b'UP', b'up'), (b'DOWN', b'down')])),
                ('owner', models.ForeignKey(related_name='votes', to='accounts.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(unique=True, max_length=500),
            preserve_default=True,
        ),
    ]
