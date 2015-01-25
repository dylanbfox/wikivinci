from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.models import Account
from accounts.forms import AccountRegisterForm

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