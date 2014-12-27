# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner_authored', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=99)),
                ('outdated', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('upvotes', models.IntegerField(default=0)),
                ('downvotes', models.IntegerField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('clicks', models.IntegerField(default=0)),
                ('url', models.URLField(max_length=500)),
                ('link_type', models.CharField(max_length=20, choices=[(b'READ', b'Read'), (b'TUTORIAL', b'Tutorial')])),
                ('description', models.TextField()),
                ('owner', models.ForeignKey(related_name='posts', to='accounts.Account')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
