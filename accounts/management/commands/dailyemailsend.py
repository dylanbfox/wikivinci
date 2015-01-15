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
		subject, from_email = 'Learn something new tonight (plus personalize your learning goals)', settings.DEFAULT_FROM_EMAIL
		host_name = settings.HOST_NAME		
		html = get_template('accounts/emails/daily-email.html')
		custom_message = (
			"You can now add personalization settings to your account! Once you do, "
			"only the topics you select as being interested in will show up in your feed "
			"and in these auto-emails.\n\nJust login, go to the \"My Feed\" page, and click "
			"\"personalize feed\" in the top right.\n\nIf anyone has feedback "
			"let me know!\n\nLastly, if you know of anyone who might have good resources/tutorials "
			"to add to Wikivinci, definitely share the site with them!\n\n - Dylan"
		)

		_posts = Post.objects.filter().select_related()
		_comments = []

		# pass any argument to test the email and only send it to self
		if args:
			accounts = Account.objects.filter(owner__email='dylanbfox@gmail.com')
		else:
			accounts = Account.objects.filter(newsletter_setting='DAILY')

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
