from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from accounts.models import Account
from comments.models import Comment
from posts.models import Post
from posts.utils import unique_tag_counts

def home(request):
	if request.user.is_authenticated() and not request.GET.get('true_home'):
		return HttpResponseRedirect(reverse('accounts:feed', kwargs={'username': request.user.username}))

	context_dict = {}
	posts = Post.objects.select_related().all().prefetch_related('upvoters', 'downvoters')
	tags = unique_tag_counts(posts)
	context_dict['tags'] = tags
	context_dict['tags_count'] = len(tags)
	context_dict['posts'] = posts[:7]
	context_dict['comments'] = Comment.objects.select_related().order_by('-created')[:5]
	return render(request, 'core/home.html', context_dict)

def contributors(request):
	context_dict = {}
	context_dict['accounts'] = Account.objects.order_by('-points').select_related()
	return render(request, 'core/contributors.html', context_dict)

def about(request):
	return render(request, 'core/about.html', {})