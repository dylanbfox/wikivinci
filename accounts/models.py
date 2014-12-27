from django.db import models
from django.conf import settings

class Account(models.Model):
	
	owner = models.OneToOneField(settings.AUTH_USER_MODEL)
	profile_pic = models.ImageField(upload_to='profile_pics')


