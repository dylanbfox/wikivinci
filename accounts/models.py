from django.db import models
from django.conf import settings

from image_cropping import ImageRatioField

class Account(models.Model):

	def __unicode__(self):
		return self.owner.username

	def save(self, *args, **kwargs):
		if self.points == 0:
			self.award_points(50)
		super(Account, self).save(*args, **kwargs)		

	def award_points(self, points=0):
		self.points += points
		self.save()
	
	owner = models.OneToOneField(settings.AUTH_USER_MODEL)
	profile_pic = models.ImageField(upload_to='profile_pics', default="static/core/images/default_profile_pic.jpg")
	cropping = ImageRatioField('profile_pic', '250x250')
	points = models.IntegerField(default=0)


