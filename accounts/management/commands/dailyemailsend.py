from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.utils import timezone

from accounts.models import Account
from posts.models import Post
from comments.models import Comment

class Command(BaseCommand):
	help = 'Manually sends daily email to every user'

	def handle(self, *args, **options):

		def create_yest_datetime_aware():
			yest_date = date.today() - timedelta(days=1)
			yest_datetime_naive = datetime.combine(yest_date, datetime.min.time())
			yest_datetime = timezone.make_aware(yest_datetime_naive, timezone.get_default_timezone())
			return yest_datetime

		yest_datetime = create_yest_datetime_aware()
		subject, from_email = 'Learn something new this week', settings.DEFAULT_FROM_EMAIL
		host_name = settings.HOST_NAME		
		html = get_template('accounts/emails/daily-email.html')
		custom_message = (
			"Thanks to everyone who signed up recently, and for all the feedback! "
			"Until there's more content being submitted, I'm only going to send these emails once "
			"per week. Hopefully we can start offering daily emails within the next couple weeks! "
			"\n\nWith that, keep sharing Wikivinci with friends who might appreciate the resource, and/or "
			"have good resources to submit :).\n\nLast week, I made some improvements to the search page, "
			"and to the submission process. You can also email posts to friends now, right from the site. "
			"Just click the \"email\" button next to the Facebook/Twitter buttons.\n\nThat's all for now! If "
			"you have any feedback/ideas let me know!\n\n- Dylan"
		)

		_posts = Post.objects.filter().select_related()
		_comments = []

		# pass any argument to test the email and only send it to self
		if args:
			accounts = Account.objects.filter(owner__email='dylanbfox@gmail.com')
		else:
			accounts = Account.objects.exclude(newsletter_setting='NONE')

		for account in accounts:
			to = account.owner.email
			objects = account.personalize_feed(_posts, _comments)[:4]
			d = Context({'objects': objects, 'custom_message': custom_message, 'HOST_NAME': host_name})
			html_content = html.render(d)
			msg = EmailMultiAlternatives(subject, '<need to edit>', from_email, [to])
			msg.attach_alternative(html_content, 'text/html')			
			try:
				msg.send()
				print "...sent to {0}".format(to)
			except:
				print "...failed to send to {0}".format(to)
