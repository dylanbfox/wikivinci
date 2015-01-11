from datetime import date, timedelta

from django.shortcuts import render
from django.http import (Http404, HttpResponseRedirect, 
						 HttpResponse, HttpResponseForbidden,
						 JsonResponse)

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from wikivinci.utils.decorators import ajax_login_required

from posts.models import Post, PostRevision
from posts.forms import PostAddForm
from posts.utils import (set_post_permissions, unique_topic_counts,
						 topic_suggestions)

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

def view_all(request):
	context_dict = {}
	posts = Post.objects.select_related().all().prefetch_related('upvoters', 'downvoters')

	if request.GET.get('topic'):
		posts = [p for p in posts if p.tags_contain(contains=request.GET['topic'])]
		context_dict['topic'] = request.GET['topic']

	if request.GET.get('contains'):
		contains = request.GET['contains']
		context_dict['contains'] = contains		
		posts = [p for p in posts if p.content_contains(contains=contains)]

	# widdle down now that we've filtered
	posts = posts[:50]
	# display by date, or by vote
	if request.GET.get('top'):
		sorted_posts = sorted(posts, key=lambda k: k.vote_count, reverse=True)
		context_dict['posts'] = sorted_posts
		context_dict['top'] = True
	else:
		groups = Post.group_by_date(posts, order_by_vote=True)
		context_dict['groups'] = groups
		context_dict['naturalday_limit'] = date.today() - timedelta(days=1)

	set_post_permissions(request, posts=posts)	
	return render(request, 'core/posts.html', context_dict)

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

def view_topics(request):
	context_dict = {}
	posts = Post.objects.select_related().all().prefetch_related('upvoters', 'downvoters')
	topics = unique_topic_counts(posts)
	context_dict['topics'] = topics
	return render(request, 'core/topics.html', context_dict)

def ajax_suggest_topics(request):
	chars = request.POST.get('chars')
	posts = Post.objects.filter(flagged=False)
	suggestions = topic_suggestions(posts, chars)
	return JsonResponse(suggestions, safe=False)