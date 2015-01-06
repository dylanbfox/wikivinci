from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

from accounts.models import Account
from posts.models import Post
from comments.models import Comment

class Command(BaseCommand):
	help = 'Manually sends daily email to every user'

	def handle(self, *args, **options):
		subject, from_email = 'Learn something new today', settings.DEFAULT_FROM_EMAIL
		html = get_template('accounts/emails/daily-email.html')
		_posts = Post.objects.select_related().all().prefetch_related('upvoters', 'downvoters')
		_comments = Comment.objects.select_related().all().prefetch_related('upvoters', 'downvoters')
		for account in Account.objects.all():
			to = account.owner.email
			host_name = settings.HOST_NAME
			try:
				objects = account.personalize_feed(_posts, _comments)[:5]
				custom_message = ('These daily emails are brand new '
					'and can be personalized.')
				d = Context({'objects': objects, 'custom_message': custom_message, 'HOST_NAME': host_name})
				html_content = html.render(d)
				msg = EmailMultiAlternatives(subject, '<need to edit>', from_email, [to])
				msg.attach_alternative(html_content, 'text/html')
				msg.send()
				print "...sent to {0}".format(to)
			except:
				print "...failed to send to {0}".format(to)
