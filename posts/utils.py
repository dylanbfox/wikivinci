def set_permissions(request, post=None, posts=None):
	if post:
		upvoter = post.upvoters.filter(owner=request.user).exists()
		downvoter = post.downvoters.filter(owner=request.user).exists()
		if upvoter or downvoter:
			post.can_vote = False
		else:
			post.can_vote = True
			
	if posts:
		account = request.user.account		
		for p in posts:
			upvoter = account in p.upvoters.all()
			downvoter = account in p.downvoters.all()
			if upvoter or downvoter:
				p.can_vote = False
			else:
				p.can_vote = True