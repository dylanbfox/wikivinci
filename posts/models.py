import re

from itertools import groupby

from django.db import models
from django.core.urlresolvers import reverse

from accounts.models import Account

class ApprovedOnlyPostManager(models.Manager):
	def get_queryset(self):
		return super(ApprovedOnlyPostManager, self).get_queryset().filter(approved=True)

class IncludePendingPostManager(models.Manager):
	def get_queryset(self):
		return super(IncludePendingPostManager, self).get_queryset()

class Post(models.Model):

	class Meta:
		ordering = ['-created']

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		# executes on first save only
		if not self.slug:
			self.slug = self.create_slug()
			if self.owner.can_post:
				self.approve(commit=False)
		super(Post, self).save(*args, **kwargs)

	def create_slug(self):
		tokens = self.title.lower().strip().split(' ')
		normalized_tokens = [re.sub(r'[^a-zA-Z0-9]', '', s) for s in tokens]
		cleaned_tokens = [s for s in normalized_tokens if s]
		slug = '-'.join(cleaned_tokens)
		return slug[:99]

	def increment_vote(self):
		self.upvotes += 1
		self.vote_count += 1
		self.save()
		self.owner.award_points(1)		

	def decrement_vote(self):
		self.downvotes -= 1
		self.vote_count -=1
		self.save()
		self.owner.award_points(-1)		

	def absolute_url(self):
		return reverse('posts:view', kwargs={'slug': self.slug})

	def tags_to_list(self):
		return [t.strip() for t in self.tags.split(',') if t]

	def tags_contain(self, contains=None):
		"""
		Converts to lowercase before comparing.
		"""
		return contains.lower() in [t.lower() for t in self.tags_to_list()]

	def content_contains(self, contains=None):
		"""
		Converts to lowercase before comparing.
		"""
		search_terms = [term.strip() for term in contains.split(',') if term]
		match = False

		for term in search_terms:
			term_title_match = term.lower() in self.title.lower()
			term_tags_match = self.tags_contain(contains=term)
			if term_title_match or term_tags_match:
				match = True

		return match

	def get_related_posts(self):
		posts = Post.objects.exclude(pk=self.pk).filter(skill_level=self.skill_level).order_by('-vote_count')
		related_posts = [p for p in posts if any(p.tags_contain(tag) for tag in self.tags_to_list())]
		return related_posts[:7]

	def approve(self, commit=True):
		from .tasks import send_approved_email
		
		self.approved = True
		if commit:
			self.save()
			send_approved_email.apply_async([self.owner.id, self.id])

		self.owner.award_points(5)	

	@staticmethod
	def group_by_date(posts, order_by_vote=False):
		groups = [{'date': t, 'posts': list(g)} for t, g in groupby(posts, key=lambda p: p.created.date())]
		if order_by_vote:
			groups = [{'date': group['date'], 'posts': sorted(group['posts'],
				key=lambda p: p.vote_count, reverse=True)} for group in groups]
		return groups

	post_types = (
		('LINK', 'link'),
		('ARTICLE', 'article'),
	)

	skill_levels = (
		('BEGINNER', 'Beginner'),
		('INTERMEDIATE', 'Intermediate'),
		('ADVANCED', 'Advanced'),
	)

	owner = models.ForeignKey(Account, related_name='posts')
	owner_authored = models.BooleanField(default=False)
	author = models.ForeignKey(Account, related_name='authored_posts', blank=True, null=True)
	title = models.CharField(max_length=200, unique=True)
	slug = models.CharField(max_length=99, unique=True)
	outdated = models.BooleanField(default=False)
	flagged = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	upvotes = models.IntegerField(default=0)
	upvoters = models.ManyToManyField(Account, related_name='upvoted_posts', blank=True)
	downvotes = models.IntegerField(default=0)
	downvoters = models.ManyToManyField(Account, related_name='downvoted_posts', blank=True)
	vote_count = models.IntegerField(default=0)
	clicks = models.IntegerField(default=0)
	tags = models.CharField(max_length=500)
	url = models.URLField(max_length=500, unique=True, null=True)
	post_type = models.CharField(max_length=20, choices=post_types)
	skill_level = models.CharField(max_length=12, choices=skill_levels)
	description = models.TextField()
	approved = models.BooleanField(default=False)

	objects = ApprovedOnlyPostManager()
	incl_pending_posts = IncludePendingPostManager()	

class PostRevision(models.Model):

	def approve(self):
		if self.revision_type == 'FLAG':
			self.post.flagged = True
			self.post.save()

		self.needs_approval = False
		self.save()
		self.owner.award_points(10)		

	revision_types = (
		('FLAG', 'flag'),
	)

	revision_type = models.CharField(max_length=99, choices=revision_types)
	edit = models.TextField()
	post = models.ForeignKey(Post, related_name='revisions')
	owner = models.ForeignKey(Account, related_name='post_revisions')
	approver = models.ForeignKey(Account, related_name='approved_post_revisions', blank=True, null=True)
	needs_approval = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	# approved_datetime = models.DateTimeField(blank=True, null=True)