from django.shortcuts import render

from comments.models import Comment
from posts.models import Post

def home(request):
	context_dict = {}
	context_dict['posts'] = Post.objects.select_related().all()[:5]
	context_dict['comments'] = Comment.objects.select_related().order_by('-created')[:3]
	return render(request, 'core/home.html', context_dict)
