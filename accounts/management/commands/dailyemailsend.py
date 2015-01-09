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
		subject, from_email = 'Learn something new today', settings.DEFAULT_FROM_EMAIL
		host_name = settings.HOST_NAME		
		html = get_template('accounts/emails/daily-email.html')
		custom_message = (""
		"You can now format/style your comments with Markdown!\n\n"
		"You can also now be flagged as the \"Author\" of a resource, even if "
		"it was submitted by another user. A link to your account, and your "
		"profile picture with a badge on it, will be displayed on the resource's page and "
		"in any comments you post. All of your authored resources will "
		"be displayed in your profile under the \"Authored\" tab.\n\nEmail me if you want "
		"to claim authorship of a resource submitted by another user!\n\n"
		"- Dylan\n\n"
		"PS - You can now unsubscribe from your account settings page."
		)

		_posts = Post.objects.filter(created__gte=yest_datetime).select_related()
		_comments = Comment.objects.filter(created__gte=yest_datetime).select_related()

		# pass any argument to test the email and only send it to self
		if args:
			accounts = Account.objects.filter(owner__email='dylanbfox@gmail.com')
		else:
			accounts = Account.objects.filter(newsletter_setting='DAILY')

		for account in accounts:
			to = account.owner.email
			objects = account.personalize_feed(_posts, _comments)[:5]
			d = Context({'objects': objects, 'custom_message': custom_message, 'HOST_NAME': host_name})
			html_content = html.render(d)
			msg = EmailMultiAlternatives(subject, '<need to edit>', from_email, [to])
			msg.attach_alternative(html_content, 'text/html')			
			try:
				msg.send()
				print "...sent to {0}".format(to)
			except:
				print "...failed to send to {0}".format(to)
