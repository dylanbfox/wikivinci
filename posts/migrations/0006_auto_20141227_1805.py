# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141224_1938'),
        ('posts', '0005_vote_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='link',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.AddField(
            model_name='link',
            name='downvoters',
            field=models.ManyToManyField(related_name='downvoted_posts', to='accounts.Account'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='upvoters',
            field=models.ManyToManyField(related_name='upvoted_posts', to='accounts.Account'),
            preserve_default=True,
        ),
    ]
