from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from wikivinci.utils.decorators import ajax_login_required

from posts.models import Post
from comments.models import Comment

@ajax_login_required
def add(request):
	if request.method != 'POST':
		return HttpResponseForbidden()

	post = Post.objects.get(pk=request.POST['post_id'])
	comment = Comment(
		owner = request.user.account,
		post = post,
		text = request.POST['text'],
	)
	comment.save()
	return HttpResponse(status=200)

@ajax_login_required
def vote(request):
	"""
	Need to throw an error if the user already voted.
	Need to allow for deleting vote.
	"""
	try:
		comment = Comment.objects.get(pk=request.POST.get('object_id'))
	except Comment.DoesNotExist:
		raise Http404

	direction = request.POST.get('vote_direction')
	if direction == 'up':
		comment.increment_vote()
		comment.upvoters.add(request.user.account)
	elif direction == 'down':
		comment.decrement_vote()
		comment.downvoters.add(request.user.account)
	comment.save()

	print comment.vote_count
	return HttpResponse(comment.vote_count)




