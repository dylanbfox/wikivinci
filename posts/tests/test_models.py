from django.test import TestCase

from mock import patch

from model_mommy import mommy

class PostModelTest(TestCase):

	@patch('posts.models.requests')
	def test_full_url_extracted_on_save(self, mock_requests):
		mock_response = mock_requests.get.return_value
		mock_response.request.url = "http://www.fullurl.com"
		post = mommy.make('posts.Post', url="http://bit.ly", slug="")
		self.assertEqual(post.url,"http://www.fullurl.com")

	def test_check_for_youtube_video_method_skips_non_youtube_urls(self):
		post = mommy.make('posts.Post',
			url="https://www.somerandomurl.com",
			slug="",
		)
		self.assertFalse(post.youtube_video)
		self.assertEqual(post.youtube_embed_url, '')

	def test_check_for_youtube_video_method_slips_if_no_video_id_in_url(self):
		post = mommy.make('posts.Post',
			url="https://www.youtube.com/", # missing 'v' query param
			slug="",
		)
		self.assertFalse(post.youtube_video)
		self.assertEqual(post.youtube_embed_url, '')
		self.assertEqual(post.url, "https://www.youtube.com/")		

	def test_youtube_video_found_on_save(self):
		post = mommy.make('posts.Post',
			url="https://www.youtube.com?v=123abc",
			slug="",
		)
		self.assertTrue(post.youtube_video)
		self.assertEqual(
			post.youtube_embed_url,
			"//www.youtube.com/embed/123abc"
		)
