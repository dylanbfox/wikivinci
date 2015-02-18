from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from mock import patch, Mock, MagicMock

from model_mommy import mommy

class TopicViewTest(TestCase):

	def test_topic_view_renders_topic_template(self):
		topic = mommy.make('topics.Topic', name='Django', slug='django')
		response = self.client.get(
			reverse('topics:view', kwargs={'slug': topic.slug})
		)
		self.assertTemplateUsed(response, 'core/single-topic.html')

	def test_topic_passed_to_template(self):
		topic = mommy.make('topics.Topic', name='Django', slug='django')
		response = self.client.get(
			reverse('topics:view', kwargs={'slug': topic.slug})
		)
		self.assertEqual(response.context['topic'], topic)

	def test_moderator_can_edit_topic(self):
		pass

	@patch('topics.views.Topic.send_application_email_to_admin')
	def test_apply_sends_email_to_admin(self,
		mock_send_application_email_to_admin
	):	
		user = User.objects.create_user(
			username="dylan",
			email="dylanbfox@gmail.com",
			password="password"
		)
		self.client.login(username="dylan", password="password")			

		topic = mommy.make('topics.Topic', name='Django', slug='django')
		response = self.client.post(
			reverse('topics:apply', kwargs={'slug': topic.slug}),
			data={'body': "My application"}
		)

		mock_send_application_email_to_admin.assert_called_once_with(
			"dylanbfox@gmail.com",
			body="My application"
		)
