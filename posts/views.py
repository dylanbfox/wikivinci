from datetime import date, timedelta

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import (Http404, HttpResponseRedirect, 
						 HttpResponse, HttpResponseForbidden,
						 JsonResponse)

from wikivinci.utils.decorators import ajax_login_required

from posts.models import Post, PostRevision
from posts.forms import PostAddForm
from posts.utils import (set_post_permissions, unique_tag_counts,
						 tag_suggestions)

from topics.models import Topic
from comments.utils import set_comment_permissions
from accounts.tasks import send_account_alert_email

@ajax_login_required
def add(request):
	context_dict = {}
	form = PostAddForm()

	if request.method == "POST":
		form = PostAddForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.owner = request.user.account
			if post.owner_authored:
				post.author = request.user.account
			post.save()
			context_dict['post'] = post
			return render(request, 'core/partials/post-add-form-success.html', context_dict)

	context_dict['form'] = form
	return render(request, 'core/partials/post-add-form.html', context_dict)

def view(request, slug):
	try:
		post = Post.objects.select_related().prefetch_related('upvoters').get(slug__iexact=slug)
	except Post.DoesNotExist:
		raise Http404

	context_dict = {}
	context_dict['post'] = post
	comments = post.comments.prefetch_related('upvoters', 'downvoters').all().select_related()
	context_dict['comments'] = comments
	set_comment_permissions(request, comments=comments)
	set_post_permissions(request, post=post)
	context_dict['related_posts'] = post.get_related_posts()
	return render(request, 'core/single-post.html', context_dict)

@ajax_login_required
def vote(request):
	"""
	* Need to throw an error if the user already voted. Front-end
	disallows voting, but back-end should also throw an error.

	* Need to allow for deleting vote.
	"""
	try:
		post = Post.objects.get(pk=request.POST.get('object_id'))
	except Post.DoesNotExist:
		raise Http404

	direction = request.POST.get('vote_direction')
	if direction == 'up':
		post.increment_vote()
		post.upvoters.add(request.user.account)
		send_account_alert_email.apply_async([post.owner.id, post.pk, "POST-UPVOTE"])		
	elif direction == 'down':
		post.decrement_vote()
		post.downvoters.add(request.user.account)
	post.save()

	return HttpResponse(post.vote_count)

@ajax_login_required
def flag(request, slug):
	try:
		post = Post.objects.get(slug__iexact=slug)
	except Post.DoesNotExist:
		raise Http404	
	
	post_revision = PostRevision(
		revision_type = 'FLAG',
		edit = request.POST['edit'],
		post = post,
		owner = request.user.account,
	)
	post_revision.save()
	return HttpResponse(status=200)

def go(request, slug):
	try:
		post = Post.objects.get(slug__iexact=slug)
	except Post.DoesNotExist:
		raise Http404

	post.clicks +=1 
	post.save()
	return HttpResponseRedirect(post.url)

def email(request, slug):
	try:
		post = Post.objects.get(slug__iexact=slug)
	except Post.DoesNotExist:
		raise Http404

	recipients = request.POST['recipients'].split(',')
	post.email(sender=request.POST['sender'], recipients=recipients)

	return HttpResponse(status=200)

def favorite(request, slug):
	try:
		post = Post.objects.get(slug__iexact=slug)
	except Post.DoesNotExist:
		raise Http404

	account = request.user.account
	if account.favorites.filter(pk=post.pk).exists():
		account.favorites.remove(post)
	else:
		account.favorites.add(post)
	
	account.save()
	return HttpResponse("success")

def view_all(request):
	context_dict = {}
	params = request.GET.copy() # pass to template for future requests

	# Get all the posts
	posts = Post.objects.select_related().all().prefetch_related('upvoters', 'downvoters')

	# and widdle down
	if request.GET.get('tag'):
		posts = [p for p in posts if p.tags_contain(contains=request.GET['tag'])]
		context_dict['tag'] = request.GET['tag']

	# and widdle down
	if request.GET.get('topic'):
		t = Topic.objects.get(name__iexact=request.GET['topic'])
		context_dict['topic'] = t
		posts = [p for p in posts if t in p.topics.all()]

	# and widdle down
	if request.GET.get('contains'):
		contains = request.GET['contains']
		context_dict['contains'] = contains		
		posts = [p for p in posts if p.content_contains(contains=contains)]

	# and widdle down
	if request.GET.get('top'):
		params.pop('top') # template handles re-setting
		sorted_posts = sorted(posts, key=lambda k: k.vote_count, reverse=True)
		context_dict['posts'] = sorted_posts[:50] # top 50 posts
		context_dict['top'] = True
	else:
		groups = Post.group_by_date(posts, order_by_vote=True)
		context_dict['groups'] = groups[:20] # past 20 days posts
		context_dict['naturalday_limit'] = date.today() - timedelta(days=1)

	context_dict['params'] = params.urlencode()
	set_post_permissions(request, posts=posts)	
	return render(request, 'core/posts.html', context_dict)

def ajax_suggest_tags(request):
	chars = request.POST.get('chars')
	posts = Post.objects.filter(flagged=False)
	suggestions = tag_suggestions(posts, chars)
	return JsonResponse(suggestions, safe=False)

def fetch_meta_data(request):
	from django.http import JsonResponse
	p = Post(url=request.POST['url'])
	meta_data = p.fetch_meta_data()
	return JsonResponse(meta_data)