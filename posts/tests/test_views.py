from django.test import TestCase
from django.core.urlresolvers import reverse

from mock import patch

from model_mommy import mommy

class ViewAllPostsViewTest(TestCase):

	def setUp(self):
		pass

	def test_posts_filtered_by_GET_params(self):
		self.fail("finish me")

	def test_GET_params_passed_to_template(self):
		self.fail("finish me")

	def test_top_GET_param_popped(self):
		self.fail("finish me")

	def test_posts_grouped_by_date(self):
		self.fail("finish me")

	def test_posts_sorted_by_vote_count(self):
		self.fail("finish me")

@patch('posts.views.Post')
class FetchMetaDataViewTest(TestCase):

	# def test_fetches_meta_data(self, mock_Post):
	# 	pass

	def test_returns_json_data(self, mock_Post):
		Post = mock_Post.return_value
		Post.fetch_meta_data.return_value = {
			"title": "Wikivinci.com | Learn",
			"description": "Wikivinci is awesome."
		}

		response = self.client.post(
			reverse('posts:fetch_meta_data'),
			data={'url': 'http://www.wikivinci.com'}
		)
		# convert string representation to dict
		json = eval(response.content)
		self.assertEqual(json["title"], "Wikivinci.com | Learn")
		self.assertEqual(json["description"], "Wikivinci is awesome.")