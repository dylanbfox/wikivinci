def set_comment_permissions(request, comments=None):
	if not request.user.is_authenticated():
		return

	account = request.user.account		
	for comment in comments:
		upvoter = account in comment.upvoters.all()
		downvoter = account in comment.downvoters.all()
		if upvoter or downvoter:
			comment.disallow_vote = True