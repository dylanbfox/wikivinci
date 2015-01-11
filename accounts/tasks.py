from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from celery import task

from accounts.models import Account
from posts.models import Post
from comments.models import Comment

@task()
def send_account_alert_email(account_pk, alert_obj_pk, alert_type):
	account = Account.objects.get(pk=account_pk)

	if alert_type == "COMMENT-UPVOTE":
		comment = Comment.objects.get(pk=alert_obj_pk)
		url = settings.HOST_NAME + comment.absolute_url()
		alert_subject = "One of your comments has been upvoted!"		
		alert_title = "You've just earned 1 point. Huzzah!"
		alert_message = ("Your comment on \"{0}\" just "
			"received a new upvote. Thanks for contributing!").format(comment.post.title)

	elif alert_type == "POST-UPVOTE":
		post = Post.objects.get(pk=alert_obj_pk)		
		url = settings.HOST_NAME + post.absolute_url()
		alert_subject = "One of your posts has been upvoted!"		
		alert_title = "You've just earned 1 point. Huzzah!"
		alert_message = ("Your post \"{0}\" just "
			"received a new upvote. Keep up the good work!").format(post.title)

	elif alert_type == "POST-COMMENT":
		comment = Comment.objects.get(pk=alert_obj_pk)		
		url = settings.HOST_NAME + comment.absolute_url()
		alert_subject = "Someone commented on one of your posts!"
		alert_title = "Your post has just received a new comment. Huzzah!"
		alert_message = ("Your post \"{0}\" just "
			"received a new comment.").format(comment.post.title)

	else:
		return

	subject, from_email = alert_subject, settings.DEFAULT_FROM_EMAIL
	html = get_template('accounts/emails/alert-email.html')
	to = account.owner.email
	d = Context({'alert_title': alert_title, 'alert_message': alert_message,
		'alert_type': alert_type, 'url': url})
	html_content = html.render(d)
	msg = EmailMultiAlternatives(subject, '<need to edit>', from_email, [to])
	msg.attach_alternative(html_content, 'text/html')
	msg.send()	