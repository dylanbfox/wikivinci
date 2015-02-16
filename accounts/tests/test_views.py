from importlib import import_module

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.conf import settings

from mock import Mock, MagicMock, patch

from model_mommy import mommy

from accounts.models import Account
from accounts.forms import AccountRegisterForm

@patch('accounts.views.Twython')
class TwitterAuthTest(TestCase):

	def create_session(self):
		engine = import_module(settings.SESSION_ENGINE)
		store = engine.SessionStore()
		store.save()
		self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
		return self.client.session

	def create_callback_session_keys(self, session):
		"""
		On callback from Twitter, we expect these 
		keys to have already been set by us before
		sending the user to Twitter.
		"""
		session['oauth_token'] = 'myoauthtoken'
		session['oauth_token_secret'] = 'myoauthtokensecret'
		session.save()	

	def setUp(self):
		self.TWITTER_AUTH_URL = "http://twitterauth.com/"
		# temporary, exchanged for real tokens
		self.fake_authentication_dict = {
			'auth_url': self.TWITTER_AUTH_URL,
			'oauth_token': "myoauthtoken",
			'oauth_token_secret': "myoauthtokensecret"
		}
		# real tokens, don't change
		self.fake_authorized_dict = {
			'oauth_token': "myoauthtoken_final",
			'oauth_token_secret': "myoauthtokensecret_final"		
		}

	def test_url_loads_view(self, mock_Twython):
		resolver = resolve(reverse('accounts:twitter_login'))
		self.assertEqual(resolver.func.__name__, 'twitter_login')

	def test_temp_oauth_tokens_stored_in_session(self, mock_Twython):
		mock_twitter = mock_Twython.return_value
		mock_auth = mock_twitter.get_authentication_tokens.return_value
		mock_auth.__getitem__.side_effect = lambda key: self.fake_authentication_dict[key]		

		self.client.get(reverse('accounts:twitter_login'))
		self.assertEqual(self.client.session['oauth_token'], mock_auth['oauth_token'])
		self.assertEqual(self.client.session['oauth_token_secret'], mock_auth['oauth_token_secret'])

	def test_login_view_redirects_to_auth_url(self, mock_Twython):
		mock_twitter = mock_Twython.return_value
		mock_auth = mock_twitter.get_authentication_tokens.return_value
		mock_auth.__getitem__.side_effect = lambda key: self.fake_authentication_dict[key]

		response = self.client.get(reverse('accounts:twitter_login'))
		self.assertRedirects(response, self.TWITTER_AUTH_URL)

	@patch('accounts.views.Account.create_twitter_user_account')
	def test_account_created_on_callback(self,
			mock_create_twitter_user_account,
			mock_Twython
		):
		session = self.create_session()
		self.create_callback_session_keys(session)
		mock_create_twitter_user_account.return_value = mommy.make('accounts.Account')		

		self.client.get(reverse('accounts:twitter_login'), {
			'oauth_verifier': 'oauthverifierkey'
		})
		self.assertTrue(mock_create_twitter_user_account.called)

	@patch('accounts.views.Account.create_twitter_user_account')
	def test_account_found_on_callback(self,
			mock_create_twitter_user_account,
			mock_Twython
		):		
		session = self.create_session()
		self.create_callback_session_keys(session)
		mock_twitter = mock_Twython.return_value
		mock_final_auth = mock_twitter.get_authorized_tokens.return_value
		mock_final_auth.__getitem__.return_value = "123" # token and secret 
		mommy.make('accounts.Account', twitter_oauth_token="123")

		self.client.get(reverse('accounts:twitter_login'), {
			'oauth_verifier': 'oauthverifierkey'
		})
		self.assertFalse(mock_create_twitter_user_account.called)		

	def test_logged_in_on_callback(self, mock_Twython):
		session = self.create_session()
		self.create_callback_session_keys(session)
		mock_twitter = mock_Twython.return_value
		mock_final_auth = mock_twitter.get_authorized_tokens.return_value
		mock_final_auth.__getitem__.return_value = "123" # token and secret 
		mommy.make('accounts.Account', twitter_oauth_token="123")

		self.client.get(reverse('accounts:twitter_login'), {
			'oauth_verifier': 'oauthverifierkey'
		})
		self.assertIn('_auth_user_id', self.client.session)

	def test_oauth_tokens_stored_to_account_on_callback(self, mock_Twython):
		pass

	def test_graceful_fail_on_denied_callback(self, mock_Twython):
		pass

	@patch('accounts.views.Account')
	def test_redirect_to_prior_page_on_callback(self, mock_Account, mock_Twython):
		session = self.create_session()
		self.create_callback_session_keys(session)
		mock_Account.objects.get.return_value = mommy.make('accounts.Account')
		
		response = self.client.get(reverse('accounts:twitter_login'), {
			'oauth_verifier': 'oauthverifierkey',
			'next': '/posts/',
		})				
		self.assertRedirects(response, '/posts/')

	@patch('accounts.views.Account')
	def test_redirect_to_posts_view_on_callback_as_default(self, mock_Account, mock_Twython):
		session = self.create_session()
		self.create_callback_session_keys(session)
		mock_Account.objects.get.return_value = mommy.make('accounts.Account')
		
		response = self.client.get(reverse('accounts:twitter_login'), {
			'oauth_verifier': 'oauthverifierkey',
		})				
		self.assertRedirects(response, '/posts/')				

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