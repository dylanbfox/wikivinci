def set_post_permissions(request, post=None, posts=None):
	if not request.user.is_authenticated():
		return

	if post:
		upvoter = post.upvoters.filter(owner=request.user).exists()
		downvoter = post.downvoters.filter(owner=request.user).exists()
		if upvoter or downvoter:
			post.disallow_vote = True
			
	if posts:
		account = request.user.account		
		for p in posts:
			upvoter = account in p.upvoters.all()
			downvoter = account in p.downvoters.all()
			if upvoter or downvoter:
				p.disallow_vote = True