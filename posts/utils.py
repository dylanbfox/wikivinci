import itertools

from operator import itemgetter
from collections import defaultdict, OrderedDict

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

def unique_tag_counts(posts):
	"""
	Forces every tag to lowercase.
	"""
	tags_lists = [p.tags_to_list() for p in posts]
	tags = list(itertools.chain(*tags_lists))
	uo_unique_tags = defaultdict(lambda: {'count': 0})
	for tag in tags:
		uo_unique_tags[tag.lower()]['count'] += 1

	unique_tags = OrderedDict(sorted(uo_unique_tags.items(),
		key=itemgetter(1), reverse=True))
	return unique_tags

def tag_suggestions(posts, chars):
	"""
	Forces every tag to lowercase.
	"""
	tag_lists = [p.tags_to_list() for p in posts]
	tags = list(itertools.chain(*tag_lists))
	matches = [t.lower() for t in tags if chars.lower() in t.lower()]
	unique_matches = list(set(matches))
	return unique_matches