from django import forms
from django.contrib.auth.models import User

from image_cropping import ImageCropWidget

from accounts.models import Account

class ProfilePicEditForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = (
			'profile_pic',
			'cropping',
		)

		widgets = {
			'profile_pic': ImageCropWidget,
		}

class AccountEditForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = (
			'title',
			'twitter_handle',
		)

	def __init__(self, *args, **kwargs):
		super(AccountEditForm, self).__init__(*args, **kwargs)
		self.fields['title'].label = "Title (eg: 'Senior Developer at Google')"

	def clean_twitter_handle(self):
		twitter_handle = self.cleaned_data.get('twitter_handle')
		if twitter_handle and twitter_handle[0] != "@":
			raise forms.ValidationError('@ symbol is required!')
		return twitter_handle

class AccountRegisterForm(forms.ModelForm):

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	email = forms.CharField(widget=forms.EmailInput())	

	class Meta:
		model = Account
		fields = (
			# 'title',
			# 'twitter_handle',
		)

	def __init__(self, *args, **kwargs):
		super(AccountRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Username'
		self.fields['password'].label = 'Password'
		self.fields['email'].label = 'Email'

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if not username:
			raise forms.ValidationError('You must set a username')
		elif User.objects.filter(username=username):
			raise forms.ValidationError('Account with this username already exists')
		return username

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not email:
			raise forms.ValidationError('You must set an email address')
		elif User.objects.filter(email=email):
			raise forms.ValidationError('Account with this email already exists')
		return email			