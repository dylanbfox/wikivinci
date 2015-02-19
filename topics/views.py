from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Topic

from posts.models import Post
from posts.utils import unique_tag_counts

def view_all(request):
	context_dict = {}
	context_dict['tags'] = unique_tag_counts(Post.objects.all())
	context_dict['topics'] = Topic.objects.all().prefetch_related('moderators')
	return render(request, 'core/topics.html', context_dict)	

def view(request, slug):
	try:
		topic = Topic.objects.prefetch_related('moderators__owner').get(slug__iexact=slug)
	except:
		raise Http404

	return render(request, 'core/single-topic.html', {'topic': topic}) 

def apply(request, slug):
	try:
		topic = Topic.objects.get(slug__iexact=slug)
	except:
		raise Http404

	topic.send_application_email_to_admin(
		request.user.email,
		body=request.POST.get('body')
	)
	return redirect('topics:view', slug=topic.slug)

@login_required
def follow(request, slug):
	try:
		topic = Topic.objects.get(slug__iexact=slug)
	except:
		raise Http404

	account = request.user.account
	if topic in account.subscribed_topics.all():
		account.subscribed_topics.remove(topic)
	else:
		account.subscribed_topics.add(topic)
	account.save()
	return HttpResponse()

@login_required
def add_post(request, slug):
	try:
		topic = Topic.objects.get(slug__iexact=slug)
	except:
		raise Http404

	post = Post.objects.get(pk=request.POST['post_pk'])
	post.topics.add(topic)
	post.save()
	return HttpResponse()