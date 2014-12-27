from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from posts.models import Link
from posts.forms import LinkAddForm

def add_link(request):
	context_dict = {}
	form = LinkAddForm()

	if request.method == "POST":
		form = LinkAddForm(request.POST)
		if form.is_valid():
			link = form.save(commit=False)
			link.owner = request.user.account
			link.save()
			context_dict['link'] = link
			return render(request, 'core/partials/link-add-form-success.html', context_dict)
		else:
			print form.errors

	context_dict['form'] = form
	return render(request, 'core/partials/link-add-form.html', context_dict)

def view(request, slug):
	try:
		link = Link.objects.get(slug__iexact=slug)
	except Link.DoesNotExist:
		raise Http404

	context_dict = {}
	context_dict['link'] = link
	return render(request, 'core/single-post.html', context_dict)

def view_all(request):
	context_dict = {}
	context_dict['links'] = Link.objects.all()
	return render(request, 'core/posts.html', context_dict)	

