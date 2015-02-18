import re

from django.db import models
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings

class Topic(models.Model):

	@property
	def absolute_url(self):
		return reverse('topics:view', kwargs={'slug': self.slug})	

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = self.create_slug()
		super(Topic, self).save(*args, **kwargs)

	def create_slug(self):
		tokens = self.name.lower().strip().split(' ')
		normalized_tokens = [re.sub(r'[^a-zA-Z0-9]', '', s) for s in tokens]
		cleaned_tokens = [s for s in normalized_tokens if s]
		slug = '-'.join(cleaned_tokens)
		return slug[:199]

	def send_application_email_to_admin(self, applicant_email, body=""):
		SUBJECT = "%s Moderator Application!" % (self.name)
		send_mail(SUBJECT, body, applicant_email,
			[settings.ADMINS[0][1]], fail_silently=True)

	name = models.CharField(max_length=200, unique=True)
	slug = models.CharField(max_length=200)
	description = models.TextField()
	image = models.ImageField(upload_to='topic_imgs')
	moderators = models.ManyToManyField('accounts.Account',
		related_name='moderating_topics',
		blank=True,
		null=True,
	)
