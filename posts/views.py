from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from posts.models import Post
from posts.forms import PostAddForm
from posts.utils import set_post_permissions

from comments.utils import set_comment_permissions

def add(request):
	context_dict = {}
	form = PostAddForm()

	if request.method == "POST":
		form = PostAddForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.owner = request.user.account
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
	return render(request, 'core/single-post.html', context_dict)

def view_all(request):
	context_dict = {}
	posts = Post.objects.select_related().all().prefetch_related('upvoters', 'downvoters')[:30]
	context_dict['posts'] = posts
	set_post_permissions(request, posts=posts)	
	return render(request, 'core/posts.html', context_dict)

@login_required
def vote(request):
	"""
	Need to throw an error if the user already voted.
	Need to allow for deleting vote.
	"""
	try:
		post = Post.objects.get(pk=request.POST.get('object_id'))
	except Post.DoesNotExist:
		raise Http404

	direction = request.POST.get('vote_direction')
	if direction == 'up':
		post.increment_vote()
		post.upvoters.add(request.user.account)
	elif direction == 'down':
		post.decrement_vote()
		post.downvoters.add(request.user.account)
	post.save()

	return HttpResponse(post.vote_count)



