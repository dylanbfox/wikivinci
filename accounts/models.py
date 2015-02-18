import random

import requests

from itertools import chain

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from twython import Twython

from image_cropping import ImageRatioField

class Account(models.Model):

	def __unicode__(self):
		return self.owner.username

	@staticmethod
	def uniqueify_twitter_screen_name(screen_name):
		matches = Account.objects.filter(owner__username=screen_name)
		if matches:
			return screen_name + "_" + str(random.randint(1,1000))
		else:
			return screen_name

	@staticmethod
	def convert_to_original_profile_image_url(default_url):
		index = default_url.find("_normal")
		return default_url[:index] + default_url[index+7:]

	@staticmethod
	def create_twitter_user_account(OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
		twitter = Twython(
			settings.TWITTER_APP_KEY,
			settings.TWITTER_APP_SECRET,
			OAUTH_TOKEN,
			OAUTH_TOKEN_SECRET
		)
		response = twitter.verify_credentials()
		unique_username = Account.uniqueify_twitter_screen_name(response['screen_name'])
		user = User.objects.create_user(username=unique_username)
		account = Account.objects.create(
			owner=user,
			twitter_handle="@"+response['screen_name'],
			twitter_oauth_token = OAUTH_TOKEN,
			twitter_oauth_secret = OAUTH_TOKEN_SECRET,
		)
		# profile pic
		img_url = Account.convert_to_original_profile_image_url(
			response['profile_image_url_https']
		)
		img_response = requests.get(img_url)
		img_temp = NamedTemporaryFile()
		img_temp.write(img_response.content)
		img_temp.flush()
		account.profile_pic.save(img_temp.name+".jpg", File(img_temp), save=True)
		account.cropping = None
		account.save()
		return account

	@staticmethod
	def username_validator():
		regex = r'^[0-9a-zA-Z]*$'
		error_message = "Alphanumeric characters only!"
		return RegexValidator(regex=regex, message=error_message)

	@property
	def username(self):
		return self.owner.username

	def award_points(self, points=0):
		self.points += points
		self.save()

	def rank(self):
		return Account.objects.filter(points__gt=self.points).count() + 1

	def personalize_feed(self, posts, comments):
		
		def obj_with_type(obj, obj_type):
			obj.obj_type = obj_type
			return obj

		if self.fav_tags:
			tags_list = self.fav_tags_to_list()
			posts = [obj_with_type(p, 'POST') for p in posts if any(p.tags_contain(tag) for tag in tags_list)]
			comments = [obj_with_type(c, 'COMMENT') for c in comments if any(c.post.tags_contain(tag) for tag in tags_list)]
		else:
			posts = [obj_with_type(p, 'POST') for p in posts]
			comments = [obj_with_type(c, 'COMMENT') for c in comments]
			
		feed_objs = list(chain(posts, comments))
		feed_objs.sort(key=lambda x: x.created, reverse=True)				
		return feed_objs

	def fav_tags_to_list(self):
		if self.fav_tags:
			return [t.strip() for t in self.fav_tags.split(',') if t]

	newsletter_settings = (
		('DAILY', 'Daily'),
		('WEEKLY', 'Weekly'),
		('NONE', 'Never. I\'m too smart already.'),
	)

	owner = models.OneToOneField(settings.AUTH_USER_MODEL)
	profile_pic = models.ImageField(upload_to='profile_pics', default="profile_pics/default_profile_pic.jpg")
	cropping = ImageRatioField('profile_pic', '250x250')
	points = models.IntegerField(default=50)
	title = models.CharField(max_length=59, blank=True, null=True)
	twitter_handle = models.CharField(max_length=200, blank=True, null=True)
	fav_tags = models.CharField(max_length=999, blank=True, null=True)
	can_comment = models.BooleanField(default=False)
	can_post = models.BooleanField(default=False)
	newsletter_setting = models.CharField(max_length=50, default='DAILY', choices=newsletter_settings)
	favorites = models.ManyToManyField('posts.Post', blank=True, null=True)
	twitter_oauth_token = models.CharField(max_length=199, blank=True, null=True)
	twitter_oauth_secret = models.CharField(max_length=199, blank=True, null=True)
