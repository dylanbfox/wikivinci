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

def unique_topic_counts(posts):
	"""
	Forces every topic to lowercase.
	"""
	topic_lists = [p.tags_to_list() for p in posts]
	topics = list(itertools.chain(*topic_lists))
	uo_unique_topics = defaultdict(lambda: {'count': 0})
	for topic in topics:
		uo_unique_topics[topic.lower()]['count'] += 1

	unique_topics = OrderedDict(sorted(uo_unique_topics.items(),
		key=itemgetter(1), reverse=True))
	return unique_topics

def topic_suggestions(posts, chars):
	"""
	Forces every topic to lowercase.
	"""
	topic_lists = [p.tags_to_list() for p in posts]
	topics = list(itertools.chain(*topic_lists))
	matches = [t.lower() for t in topics if chars.lower() in t.lower()]
	unique_matches = list(set(matches))
	return unique_matches