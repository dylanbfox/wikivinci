from django.db import models
from django.conf import settings

class Account(models.Model):

	def __unicode__(self):
		return self.owner.username
	
	owner = models.OneToOneField(settings.AUTH_USER_MODEL)
	profile_pic = models.ImageField(upload_to='profile_pics')
	points = models.IntegerField(default=5)


