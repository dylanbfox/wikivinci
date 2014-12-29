from django.db import models

from posts.models import Post
from accounts.models import Account

class Comment(models.Model):

	class Meta:
		ordering = ['-vote_count']

	def save(self, *args, **kwargs):
		if not self.created:
			self.owner.points += 5
			self.owner.save()
		super(Comment, self).save(*args, **kwargs)		

	def increment_vote(self):
		self.upvotes += 1
		self.vote_count += 1
		self.save()

	def decrement_vote(self):
		self.downvotes -= 1
		self.vote_count -=1
		self.save()	

	owner = models.ForeignKey(Account, related_name='comments')
	post = models.ForeignKey(Post, related_name='comments')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	last_updated_by = models.ForeignKey(Account, related_name='last_updated_comments', null=True, blank=True)
	upvotes = models.IntegerField(default=0)
	upvoters = models.ManyToManyField(Account, related_name='upvoted_comments', null=True, blank=True)
	downvotes = models.IntegerField(default=0)
	downvoters = models.ManyToManyField(Account, related_name='downvoted_comments', null=True, blank=True)
	vote_count = models.IntegerField(default=0)	
	text = models.TextField()
