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
		custom_message = ("I'm excited to launch this email feature! "
			"It'll keep you up to date with interesting new content being "
			"added to Wikivinci. By tomorrow you'll be able to unsubscribe if you "
			"want ;). You'll also now be notified when someone upvotes one of your "
			"posts or comments, and when someone comments on something you posted. "
			"By the end of this week, you'll be able to personalize this email (and your feed) "
			"so you can tailor it towards topics you care about. Hopefully this "
			"helps you learn something new every day. Thanks everyone for all the feedback, "
			"and the great content you've added so far! Keep it coming! "
			" - Dylan"
			)

		_posts = Post.objects.filter(created__gte=yest_datetime).select_related()
		_comments = Comment.objects.filter(created__gte=yest_datetime).select_related()

		# pass any argument to test the email and only send it to self
		if args:
			accounts = Account.objects.filter(owner__email='dylanbfox@gmail.com')
		else:
			accounts = Account.ojects.all()

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
