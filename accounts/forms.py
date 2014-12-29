from django import forms
from django.contrib.auth.models import User

from accounts.models import Account

class AccountRegisterForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = (
			'profile_pic',
		)

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	email = forms.CharField(widget=forms.CharField())

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if not username:
			raise forms.ValidationError('You must set a username')
		elif User.objects.get(username=username).exists():
			raise forms.ValidationError('Account with this username already exists')
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not email:
			raise forms.ValidationError('You must set an email address')
		elif User.objects.get(email=email).exists():
			raise forms.ValidationError('Account with this email already exists')
		return email		


	def __init__(self, *args, **kwargs):
		super(AccountRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Username'
		self.fields['password'].label = 'Password'
		self.fields['email'].label = 'Email'