from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve

from mock import Mock, MagicMock, patch

from accounts.models import Account
from accounts.forms import AccountRegisterForm

@patch('accounts.views.Twython')
class TwitterAuthTest(TestCase):

	def setUp(self):
		self.TWITTER_AUTH_URL = "http://twitterauth.com/"	
		self.fake_authentication_dict = {
			'auth_url': self.TWITTER_AUTH_URL,
			'oauth_token': "myoauthtoken",
			'oauth_token_secret': "myoauthtokensecret"
		}

	def test_url_loads_view(self, mock_Twython):
		resolver = resolve(reverse('accounts:twitter_login'))
		self.assertEqual(resolver.func.__name__, 'twitter_login')

	def test_login_view_redirects_to_auth_url(self, mock_Twython):
		mock_twitter = mock_Twython.return_value
		mock_auth = mock_twitter.get_authentication_tokens.return_value
		mock_auth.__getitem__.side_effect = lambda key: self.fake_authentication_dict[key]

		response = self.client.get(reverse('accounts:twitter_login'))
		self.assertRedirects(response, self.TWITTER_AUTH_URL)

	def test_temp_oauth_tokens_stored_in_session(self, mock_Twython):
		mock_twitter = mock_Twython.return_value
		mock_auth = mock_twitter.get_authentication_tokens.return_value
		mock_auth.__getitem__.side_effect = lambda key: self.fake_authentication_dict[key]		

		self.client.get(reverse('accounts:twitter_login'))
		self.assertEqual(self.client.session['oauth_token'], mock_auth['oauth_token'])
		self.assertEqual(self.client.session['oauth_token_secret'], mock_auth['oauth_token_secret'])

	def test_oauth_tokens_stored_to_account_on_callback(self, mock_Twython):
		pass

	def test_session_flushed_on_callback(self, mock_Twython):
		pass

	def test_account_created_on_callback(self, mock_Twython):
		pass

	def test_graceful_fail_on_denied_callback(self, mock_Twython):
		pass

	def test_redirect_to_prior_page_on_callback(self, mock_Twython):
		pass 

class AccountRegisterFormTest(TestCase):

	def test_alphanumeric_only_allowed_in_username(self):
		data = {
			'username': 'dylanbfox@gmail.com',
			'password': 'password',
			'email': 'dylanbfox@gmail.com'
		}

		form = AccountRegisterForm(data=data)
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['username'], ['Alphanumeric characters only!'])

class AccountModelTest(TestCase):

	def test_username_validator_raises_error(self):
		validator = Account.username_validator()
		with self.assertRaises(ValidationError):
			validator("dylanbfox@gmail.com")