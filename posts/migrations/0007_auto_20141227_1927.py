# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141224_1938'),
        ('posts', '0006_auto_20141227_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('owner_authored', models.BooleanField(default=False)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.CharField(unique=True, max_length=99)),
                ('outdated', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('upvotes', models.IntegerField(default=0)),
                ('downvotes', models.IntegerField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('clicks', models.IntegerField(default=0)),
                ('tags', models.CharField(max_length=500)),
                ('url', models.URLField(max_length=500, unique=True, null=True)),
                ('post_type', models.CharField(max_length=20, choices=[(b'LINK', b'link'), (b'ARTICLE', b'article')])),
                ('description', models.TextField()),
                ('downvoters', models.ManyToManyField(related_name='downvoted_posts', to='accounts.Account')),
                ('owner', models.ForeignKey(related_name='posts', to='accounts.Account')),
                ('upvoters', models.ManyToManyField(related_name='upvoted_posts', to='accounts.Account')),
            ],
            options={
                'ordering': ['created'],
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='link',
            name='downvoters',
        ),
        migrations.RemoveField(
            model_name='link',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='link',
            name='upvoters',
        ),
        migrations.DeleteModel(
            name='Link',
        ),
    ]
