from datetime import date, timedelta

from twython import Twython

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from accounts.models import Account
from accounts.forms import (AccountRegisterForm, ProfilePicEditForm,
							AccountEditForm)

from posts.models import Post
from posts.utils import unique_topic_counts

from comments.models import Comment

def account_register(request):
	context_dict = {}
	if request.method == "GET":
		form = AccountRegisterForm()
		context_dict['form'] = form
		return render(request, 'core/partials/account-register-form.html', context_dict)

	form = AccountRegisterForm(request.POST, request.FILES)
	if not form.is_valid():
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

def account_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def profile(request, username):
	context_dict = {}
	user = User.objects.get(username__iexact=username)
	account = user.account
	context_dict['account'] = account
	context_dict['posts'] = Post.objects.select_related().filter(owner=account).order_by('-vote_count')
	context_dict['authored'] = account.authored_posts.select_related().all().order_by('-vote_count')
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
	account_edit_form = AccountEditForm(instance=account)
	if request.method == "POST":
		cropping = request.POST.get('cropping')
		if cropping is not None and cropping != account.cropping:
			profile_pic_form = ProfilePicEditForm(request.POST, instance=account)			
			if profile_pic_form.is_valid():
				profile_pic_form.save()

		else:
			account_edit_form = AccountEditForm(request.POST, instance=account)
			if account_edit_form.is_valid():
				account = account_edit_form.save()

			if request.FILES.get('profile-pic'):
				account.profile_pic = request.FILES['profile-pic']
				account.cropping = None
				account.save()

	context_dict['account'] = account
	context_dict['account_edit_form'] = account_edit_form
	context_dict['profile_pic_form'] = ProfilePicEditForm(instance=account)
	return render(request, 'core/account-edit.html', context_dict)

@login_required
def feed(request, username):
	if request.user.username != username:
		return HttpResponseForbidden()

	account = request.user.account
	if request.method == 'POST':
		account.fav_topics = request.POST['favorite_topics']
		account.save()

	context_dict = {}
	_posts = Post.objects.select_related().all().prefetch_related('upvoters', 'downvoters')
	_comments = Comment.objects.select_related().all().prefetch_related('upvoters', 'downvoters')
	feed_objs = account.personalize_feed(_posts, _comments)

	context_dict['groups'] = Post.group_by_date(feed_objs[:30])
	context_dict['naturalday_limit'] = date.today() - timedelta(days=1)	
	context_dict['account'] = account
	
	topics = unique_topic_counts(_posts)
	context_dict['topics'] = topics
	context_dict['account'] = account
	context_dict['fav_topics'] = account.fav_topics_to_list()
	return render(request, 'core/feed.html', context_dict)

def twitter_login(request):
	## denied query param on GET request if denied/
	from django.conf import settings

	if request.GET.get('oauth_verifier'):
		oauth_verifier = request.GET['oauth_verifier']
		twitter = Twython(
			settings.TWITTER_APP_KEY,
			settings.TWITTER_APP_SECRET,
			request.session['oauth_token_tmp'],
			request.session['oauth_token_secret_tmp']			
		)
		final_auth = twitter.get_authorized_tokens(oauth_verifier)
		print "Printing authenticated users OAuth Token and Secret..."
		print final_auth['oauth_token']
		print final_auth['oauth_token_secret']
		request.session.flush()
		return HttpResponse("done")

	CALLBACK_URL = settings.HOST_NAME + '/accounts/login/twitter/'
	twitter = Twython(settings.TWITTER_APP_KEY,
		settings.TWITTER_APP_SECRET
	)
	auth = twitter.get_authentication_tokens(
		callback_url=CALLBACK_URL
	)
	# # user's oauth tokens
	# print "Printing temporary OAuth Token and Secret..."
	# print auth['oauth_token']
	# print auth['oauth_token_secret']
	request.session['oauth_token'] = auth['oauth_token']
	request.session['oauth_token_secret'] = auth['oauth_token_secret']
	return redirect(auth['auth_url'])
