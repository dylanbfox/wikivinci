from django.test import TestCase
from django.core.exceptions import ValidationError

from model_mommy import mommy

from mock import patch, Mock, MagicMock 

from accounts.models import Account
from posts.models import Post
from comments.models import Comment

class AccountModelTest(TestCase):

	def test_username_validator_raises_error(self):
		validator = Account.username_validator()
		with self.assertRaises(ValidationError):
			validator("dylanbfox@gmail.com")

	def test_subscribed_to_topics_method_returns_correct_bool(self):
		topic = mommy.make('topics.Topic')
		account_boring = mommy.make('accounts.Account')
		account_exciting = mommy.make('accounts.Account', subscribed_topics=[topic])

		self.assertTrue(account_exciting.subscribed_to_topics)
		self.assertFalse(account_boring.subscribed_to_topics)

	def test_personalize_feed_method_returns_only_subscribed_topics_activity(self):
		topic_subscribed = mommy.make('topics.Topic', name='Django')
		topic_unsubscribed = mommy.make('topics.Topic', name='Poopie')
		account = mommy.make('accounts.Account', subscribed_topics=[topic_subscribed])
		
		# should be in feed_objects
		post1 = mommy.make('posts.Post', title="A post", topics=[topic_subscribed], approved=True)
		comment1 = mommy.make('comments.Comment', text="A comment", post=post1)
		# should not be in feed objects
		post2 = mommy.make('posts.Post', title="B post", topics=[topic_unsubscribed], approved=True)
		comment2 = mommy.make('comments.Comment', text="B comment", post=post2)

		_posts = Post.objects.all()
		_comments = Comment.objects.all()
		feed_objects = account.personalize_feed(_posts, _comments)

		self.assertIn(post1, feed_objects)
		self.assertIn(comment1, feed_objects)
		self.assertNotIn(post2, feed_objects)
		self.assertNotIn(comment2, feed_objects)

	def test_personalize_feed_adds_object_type_property_to_posts_and_comments(self):
		topic = mommy.make('topics.Topic', name="Django")
		account = mommy.make('accounts.Account', subscribed_topics=[topic])
		post = mommy.make('posts.Post', topics=[topic], approved=True)
		comment = mommy.make('comments.Comment', post=post)

		_posts = Post.objects.all()
		_comments = Comment.objects.all()
		feed_objects = account.personalize_feed(_posts, _comments)

		self.assertTrue(hasattr(feed_objects[0], 'obj_type'))

	def test_personalize_feed_adds_correct_object_type_property(self):
		topic = mommy.make('topics.Topic', name="Django")
		account = mommy.make('accounts.Account', subscribed_topics=[topic])
		post = mommy.make('posts.Post', topics=[topic], approved=True)
		comment = mommy.make('comments.Comment', post=post)

		_posts = Post.objects.all()
		_comments = Comment.objects.all()
		feed_objects = account.personalize_feed(_posts, _comments)

		updated_post = feed_objects[feed_objects.index(post)]
		updated_comment = feed_objects[feed_objects.index(comment)]

		self.assertEqual(updated_post.obj_type, "POST")
		self.assertEqual(updated_comment.obj_type, "COMMENT")

@patch('accounts.models.Twython')
class AccountModelTwitterAuthTest(TestCase):

	def setUpMockTwitterResponses(self, mock_Twython):
		mock_twitter = mock_Twython.return_value
		mock_twitter.verify_credentials.return_value = {
			'screen_name': 'dylanbfox',
			'profile_image_url_https': 'https://pbs.twimg.com/profile_images/559733860867403776/rp1vjXHK_normal.png'
		}

	def test_create_twitter_user_account_saves_user(self, mock_Twython):
		self.setUpMockTwitterResponses(mock_Twython)
		Account.create_twitter_user_account("FAKEOAUTH", "FAKEOAUTHSECRET")
		new_account = Account.objects.first()
		self.assertEqual(1, Account.objects.all().count())

	@patch('accounts.models.random')
	def test_duplicate_username_handling(self, mock_random, mock_Twython):
		self.setUpMockTwitterResponses(mock_Twython)
		mock_random.randint.return_value = 32
		user_1 = mommy.make('accounts.Account', owner__username='dylanbfox')
		account = Account.create_twitter_user_account("FAKEOAUTH", "FAKEOAUTHSECRET")
		self.assertEqual('dylanbfox_32', account.owner.username)

	def test_profile_pic_is_saved(self, mock_Twython):
		self.fail("finish me :(")
