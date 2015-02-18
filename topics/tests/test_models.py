from django.test import TestCase
from django.conf import settings

from model_mommy import mommy

from mock import patch, Mock, MagicMock 

class TopicModelTest(TestCase):
	"""
	Topics are always saved with blank slugs on initial save.
	"""

	def test_slug_set_on_save(self):
		topic = mommy.make('topics.Topic', name='Django Topic', slug='')
		self.assertEqual(topic.slug, 'django-topic')

	def test_absolute_url_method_returns_url(self):
		topic = mommy.make('topics.Topic', name='Django', slug='')
		url = topic.absolute_url
		self.assertEqual(url, '/topics/django/')

	def test_adding_moderator(self):
		pass

	@patch('topics.models.send_mail')
	def test_moderator_application_email(self, mock_send_mail):
		topic = mommy.make('topics.Topic', name='Django')
		topic.send_application_email_to_admin(
			"dylanbfox@gmail.com",
			body="My application"
		)
		mock_send_mail.assert_called_once_with(
			"Django Moderator Application!",
			"My application",
			"dylanbfox@gmail.com",
			[settings.ADMINS[0][1]],
			fail_silently=True,
		)
