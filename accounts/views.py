from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from accounts.models import Account
from accounts.forms import AccountRegisterForm

def account_register(request):
	context_dict = {}
	if request.method == "GET":
		form = AccountRegisterForm()
		context_dict['form'] = form
		return render(request, 'core/partials/account-register-form.html', context_dict)

	form = AccountRegisterForm(request.POST, request.FILES)
	if not form.is_valid():
		print "errors"
		context_dict['form'] = form		
		return render(request, 'core/partials/account-register-form.html', context_dict)

	user = User.objects.create_user(
		form.cleaned_data['username'],
		form.cleaned_data['email'],
		form.cleaned_data['password'],
	)

	account = form.save(commit=False)
	account.owner = user
	account.save()
	return HttpResponse("success")

def account_login(request):
	username = request.POST['username']
	password = request.POST['password']

	# check if user passed in email address instead
	try:
		user = User.objects.get(email=username)
	except User.DoesNotExist:
		pass
	else:
		username = user.username

	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return HttpResponse("success")
	else:
		return HttpResponse("fail")
