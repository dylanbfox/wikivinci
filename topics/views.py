from django.shortcuts import render
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
	return HttpResponse()