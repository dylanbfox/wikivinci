from django.test import TestCase
from django.core.exceptions import ValidationError

from model_mommy import mommy

from mock import patch, Mock, MagicMock 

from accounts.models import Account

class AccountModelTest(TestCase):

	def test_username_validator_raises_error(self):
		validator = Account.username_validator()
		with self.assertRaises(ValidationError):
			validator("dylanbfox@gmail.com")

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
		pass
