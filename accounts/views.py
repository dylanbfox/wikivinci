from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from accounts.models import Account
from accounts.forms import AccountRegisterForm, ProfilePicEditForm

from posts.models import Post
from comments.models import Comment

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
	user = authenticate(username=form.cleaned_data['username'],
		password=form.cleaned_data['password'])
	login(request, user)
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

def profile(request, username):
	context_dict = {}
	user = User.objects.get(username__iexact=username)
	account = user.account
	context_dict['account'] = account
	context_dict['posts'] = Post.objects.select_related().filter(owner=account).order_by('-vote_count')
	context_dict['authored'] = Post.objects.select_related().filter(owner=account, owner_authored=True).order_by('-vote_count')
	context_dict['upvoted'] = Post.objects.select_related().filter(upvoters=account).order_by('-vote_count')
	context_dict['comments'] = Comment.objects.select_related().filter(owner=account).order_by('-vote_count')
	context_dict['rank'] = account.rank()
	return render(request, 'core/profile.html', context_dict)

@login_required
def settings(request, username):
	if request.user.username != username:
		return HttpResponseForbidden()

	context_dict = {}
	account = request.user.account

	if request.method == "POST":
		if request.POST.get('cropping') != account.cropping:
			profile_pic_form = ProfilePicEditForm(request.POST, instance=account)
			if profile_pic_form.is_valid():
				profile_pic_form.save()

		account.title = request.POST.get('title')
		if request.FILES.get('profile-pic'):
			account.profile_pic = request.FILES['profile-pic']
		account.save()

	profile_pic_form = ProfilePicEditForm(instance=account)
	context_dict['account'] = account
	context_dict['profile_pic_form'] = profile_pic_form
	return render(request, 'core/account-edit.html', context_dict)
