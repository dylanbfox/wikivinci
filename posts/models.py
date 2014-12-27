import re

from django.db import models
from django.core.urlresolvers import reverse

from accounts.models import Account

class Post(models.Model):

	class Meta:
		abstract = True

	def increment_vote(self):
		self.upvotes += 1
		self.vote_count += 1
		self.save()

	def decrement_vote(self):
		self.downvotes -= 1
		self.vote_count -=1
		self.save()

	owner = models.ForeignKey(Account, related_name='posts')
	owner_authored = models.BooleanField(default=False)
	title = models.CharField(max_length=200, unique=True)
	slug = models.CharField(max_length=99, unique=True)
	outdated = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	upvotes = models.IntegerField(default=0)
	upvoters = models.ManyToManyField(Account, related_name='upvoted_posts')
	downvotes = models.IntegerField(default=0)
	downvoters = models.ManyToManyField(Account, related_name='downvoted_posts')
	vote_count = models.IntegerField(default=0)
	clicks = models.IntegerField(default=0)
	tags = models.CharField(max_length=500)

class Link(Post):

	def save(self, *args, **kwargs):
		self.slug = '-'.join([re.sub('\W+', '', s) for s in self.title.lower().split(' ')])
		super(Link, self).save(*args, **kwargs)	

	def full_url(self):
		return reverse('posts:view', kwargs={'slug': self.slug})	

	link_types = (
		('READ', 'Read'),
		('TUTORIAL', 'Tutorial'),
	)

	url = models.URLField(max_length=500, unique=True)
	link_type = models.CharField(max_length=20, choices=link_types)
	description = models.TextField()
