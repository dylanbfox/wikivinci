from itertools import chain

from django.db import models
from django.conf import settings

from image_cropping import ImageRatioField

class Account(models.Model):

	def __unicode__(self):
		return self.owner.username

	# def save(self, *args, **kwargs):
	# 	super(Account, self).save(*args, **kwargs)		

	def award_points(self, points=0):
		self.points += points
		self.save()

	def rank(self):
		return Account.objects.filter(points__gt=self.points).count() + 1

	def personalize_feed(self, posts, comments):
		
		def obj_with_type(obj, obj_type):
			obj.obj_type = obj_type
			return obj

		if self.fav_topics:
			topics_list = self.fav_topics_to_list()
			posts = [obj_with_type(p, 'POST') for p in posts if any(p.tags_contain(topic) for topic in topics_list)]
			comments = [obj_with_type(c, 'COMMENT') for c in comments if any(c.post.tags_contain(topic) for topic in topics_list)]
		else:
			posts = [obj_with_type(p, 'POST') for p in posts]
			comments = [obj_with_type(c, 'COMMENT') for c in comments]
			
		feed_objs = list(chain(posts, comments))
		feed_objs.sort(key=lambda x: x.created, reverse=True)				
		return feed_objs

	def fav_topics_to_list(self):
		return [t.strip() for t in self.fav_topics.split(',') if t]

	owner = models.OneToOneField(settings.AUTH_USER_MODEL)
	profile_pic = models.ImageField(upload_to='profile_pics', default="profile_pics/default_profile_pic.jpg")
	cropping = ImageRatioField('profile_pic', '250x250')
	points = models.IntegerField(default=50)
	title = models.CharField(max_length=59, blank=True, null=True)
	twitter_handle = models.CharField(max_length=200, blank=True, null=True)
	fav_topics = models.CharField(max_length=999, blank=True, null=True)


