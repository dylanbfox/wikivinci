from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse

from .models import Topic

from wikivinci.utils.decorators import ajax_login_required

def view_all(request):
	pass

def view(request, slug):
	try:
		topic = Topic.objects.prefetch_related('moderators__owner').get(slug__iexact=slug)
	except:
		raise Http404

	return render(request, 'core/single-topic.html', {'topic': topic})

# @ajax_login_required
# def apply(request, slug):
# 	try:
# 		topic = Topic.objects.prefetch_related('moderators__owner').get(slug__iexact=slug)
# 	except:
# 		raise Http404

# 	applicant = request.POST['email']
# 	body = request.POST['body']
# 

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

