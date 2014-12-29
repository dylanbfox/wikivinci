# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141224_1938'),
        ('posts', '0007_auto_20141227_1927'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('revision_type', models.CharField(max_length=99, choices=[(b'FLAG', b'flag')])),
                ('edit', models.TextField()),
                ('approver', models.ForeignKey(related_name='approved_post_revisions', to='accounts.Account')),
                ('owner', models.ForeignKey(related_name='post_revisions', to='accounts.Account')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
