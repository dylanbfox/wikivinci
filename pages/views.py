from django.shortcuts import render

from accounts.models import Account
from comments.models import Comment
from posts.models import Post

def home(request):
	context_dict = {}
	context_dict['posts'] = Post.objects.select_related().all()[:5]
	context_dict['comments'] = Comment.objects.select_related().order_by('-created')[:3]
	return render(request, 'core/home.html', context_dict)

def contributors(request):
	context_dict = {}
	context_dict['accounts'] = Account.objects.order_by('-points').select_related()
	return render(request, 'core/contributors.html', context_dict)