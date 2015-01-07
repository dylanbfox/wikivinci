from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from wikivinci.utils.decorators import ajax_login_required

from posts.models import Post
from comments.models import Comment
from accounts.tasks import send_account_alert_email

@ajax_login_required
def add(request):
	if request.method != 'POST':
		return HttpResponseForbidden()

	if not request.user.account.can_comment:
		return HttpResponse("denied")

	post = Post.objects.get(pk=request.POST['post_id'])
	comment = Comment(
		owner = request.user.account,
		post = post,
		text = request.POST['text'],
	)
	comment.save()
	send_account_alert_email.apply_async([post.owner.id, comment.pk, "POST-COMMENT"])
	return HttpResponse(status=200)

@ajax_login_required
def vote(request):
	"""
	* Need to throw an error if the user already voted. Front-end
	disallows voting, but back-end should also throw an error.

	* Need to allow for deleting vote.
	"""
	try:
		comment = Comment.objects.get(pk=request.POST.get('object_id'))
	except Comment.DoesNotExist:
		raise Http404

	direction = request.POST.get('vote_direction')
	if direction == 'up':
		comment.increment_vote()
		comment.upvoters.add(request.user.account)
		send_account_alert_email.apply_async([comment.owner.id, comment.pk, "COMMENT-UPVOTE"])		
	elif direction == 'down':
		comment.decrement_vote()
		comment.downvoters.add(request.user.account)
	comment.save()

	return HttpResponse(comment.vote_count)

@ajax_login_required
def delete(request):
	try:
		comment = Comment.objects.get(pk=request.POST.get('object_id'))
	except Comment.DoesNotExist:
		raise Http404

	comment.delete()
	return HttpResponse(status=200)

