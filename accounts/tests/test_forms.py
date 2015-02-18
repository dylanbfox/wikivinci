from django.test import TestCase

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