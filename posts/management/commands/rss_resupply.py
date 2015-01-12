import feedparser

from djang.core.management.base import BaseCommand

from accounts.models import Account
from posts.models import Post

class Command(BaseCommand):
	help = 'Fetches posts from RSS feeds of a few good blogs'

	def handle(self, *args, **options):
		blog_urls = [
			'http://www.obeythetestinggoat.com/feeds/all.atom.xml',
		]

		for url in blog_urls:
			d = feedparser.parse(url)
			for entry in d.entries
				title = entry.title
				url = entry.url


