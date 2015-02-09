from model_mommy import mommy

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Comment

class CommentReplyTest(TestCase):

	def test_comment_saved_as_reply(self):
		comment = mommy.make(
			'comments.Comment',
			type='2',
		)
		comments_count = Comment.objects.filter(type='1').count()
		replies_count = Comment.objects.filter(type='2').count()
		self.assertEqual(1, replies_count)
		self.assertEqual(0, comments_count)

	def test_comment_saved_as_non_reply(self):
		comment = mommy.make(
			'comments.Comment',
			type='1'
		)
		comments_count = Comment.objects.filter(type='1').count()
		replies_count = Comment.objects.filter(type='2').count()
		self.assertEqual(0, replies_count)
		self.assertEqual(1, comments_count)

	def test_POST_to_add_view_saves_reply(self):
		# call view w/ POST data
		response = self.client.post(
			reverse('comments:add'),
			data={},
		)
		# check view responds with OK
		self.assertEqual(response.status_code, 200)
		# check DB has 1 type 2, 0 type 1
		comments_count = Comment.objects.filter(type='1').count()
		replies_count = Comment.objects.filter(type='2').count()
		self.assertEqual(1, replies_count)
		self.assertEqual(0, comments_count)
