# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141224_1938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('upvotes', models.IntegerField(default=0)),
                ('downvotes', models.IntegerField(default=0)),
                ('vote_count', models.IntegerField(default=0)),
                ('text', models.TextField()),
                ('downvoters', models.ManyToManyField(related_name='downvoted_comments', null=True, to='accounts.Account', blank=True)),
                ('last_updated_by', models.ForeignKey(related_name='last_updated_comments', blank=True, to='accounts.Account', null=True)),
                ('owner', models.ForeignKey(related_name='comments', to='accounts.Account')),
                ('upvoters', models.ManyToManyField(related_name='upvoted_comments', null=True, to='accounts.Account', blank=True)),
            ],
            options={
                'ordering': ['vote_count'],
            },
            bases=(models.Model,),
        ),
    ]
