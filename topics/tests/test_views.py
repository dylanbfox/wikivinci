from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from mock import patch, Mock, MagicMock

from model_mommy import mommy

from topics.models import Topic
from accounts.models import Account
from posts.models import Post

class FollowViewTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(
			username="dylan",
			password="password"
		)
		self.account = mommy.make('accounts.Account', owner=self.user)
		self.topic = mommy.make('topics.Topic', name="Django")		
		self.client.login(username="dylan", password="password")		

	def test_follow_topic_adds_m2m_relationship_to_account(self):
		self.client.post(reverse('topics:follow',
			kwargs={'slug': self.topic.slug})
		)

		# refresh instances
		self.topic = Topic.objects.first()
		self.account = Account.objects.first()
		self.assertIn(self.topic, self.account.subscribed_topics.all())

	def test_follow_topic_removes_existing_m2m_relationship_with_account(self):
		self.account.subscribed_topics.add(self.topic)
		self.client.post(reverse('topics:follow',
			kwargs={'slug': self.topic.slug})
		)

		# refresh instances
		self.topic = Topic.objects.first()
		self.account = Account.objects.first()
		self.assertNotIn(self.topic, self.account.subscribed_topics.all())


class ViewAllTopicsViewTest(TestCase):

	def test_tags_passed_to_view(self):
		post = mommy.make('posts.Post', tags="django", approved=True)
		response = self.client.get(reverse('topics:view_all'))
		self.assertIn("django", response.context['tags'])

	def test_topics_passed_to_view(self):
		topic = mommy.make("topics.Topic", name="Django")
		response = self.client.get(reverse('topics:view_all'))
		self.assertIn(topic, response.context['topics'])

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

class TopicAddPostTest(TestCase):

	def setUp(self):
		self.user = User.objects.create_user(
			username="dylan",
			password="password"
		)
		self.client.login(username="dylan", password="password")

	def test_view_adds_post_to_topic(self):
		post = mommy.make('posts.Post', approved=True)
		topic = mommy.make('topics.Topic')

		url = reverse('topics:add_post', kwargs={'slug': topic.slug})
		self.client.post(url, data={'post_pk': post.pk})

		post = Post.objects.first() # refresh instance
		self.assertTrue(topic in post.topics.all())

	def test_non_moderator_permission_denied(self):
		self.fail("finish me :(")
