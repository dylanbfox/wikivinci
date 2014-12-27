from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from posts.models import Link
from posts.forms import LinkAddForm
from posts.utils import set_permissions

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

	context_dict['form'] = form
	return render(request, 'core/partials/link-add-form.html', context_dict)

def view(request, slug):
	try:
		link = Link.objects.get(slug__iexact=slug)
	except Link.DoesNotExist:
		raise Http404

	context_dict = {}
	context_dict['link'] = link
	set_permissions(request, post=link)
	return render(request, 'core/single-post.html', context_dict)

def view_all(request):
	context_dict = {}
	links = Link.objects.select_related().all().prefetch_related('upvoters', 'downvoters')[:30]
	context_dict['links'] = links
	set_permissions(request, posts=links)	
	return render(request, 'core/posts.html', context_dict)

@login_required
def vote(request):
	"""
	Need to throw an error if the user already voted.
	Need to allow for deleting vote.
	"""
	try:
		link = Link.objects.get(pk=request.POST.get('object_id'))
	except Link.DoesNotExist:
		raise Http404

	direction = request.POST.get('vote_direction')
	if direction == 'up':
		link.increment_vote()
		link.upvoters.add(request.user.account)
	elif direction == 'down':
		link.decrement_vote()
		link.downvoters.add(request.user.account)
	link.save()

	return HttpResponse(link.vote_count)



