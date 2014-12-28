import re

from django.db import models
from django.core.urlresolvers import reverse

from accounts.models import Account

class Post(models.Model):

	class Meta:
		ordering = ['created']

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self.create_slug()
		super(Post, self).save(*args, **kwargs)

	def create_slug(self):
		tokens = self.title.lower().strip().split(' ')
		normalized_tokens = [re.sub(r'[^a-zA-Z0-9]', '', s) for s in tokens]
		cleaned_tokens = [s for s in normalized_tokens if s]
		slug = '-'.join(cleaned_tokens)
		return slug

	def increment_vote(self):
		self.upvotes += 1
		self.vote_count += 1
		self.save()

	def decrement_vote(self):
		self.downvotes -= 1
		self.vote_count -=1
		self.save()

	def full_url(self):
		return reverse('posts:view', kwargs={'slug': self.slug})	

	link_types = (
		('LINK', 'link'),
		('ARTICLE', 'article'),
	)		

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
	url = models.URLField(max_length=500, unique=True, null=True)
	post_type = models.CharField(max_length=20, choices=link_types)
	description = models.TextField()


