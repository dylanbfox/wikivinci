from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from celery import task

from accounts.models import Account
from posts.models import Post
from comments.models import Comment

@task()
def send_alert_email(account_pk, alert_obj_pk, alert_type):
	account = Account.objects.get(pk=account_pk)

	if alert_type == "COMMENT-UPVOTE":
		comment = Comment.objects.get(pk=alert_obj_pk)
		url = settings.HOST_NAME + comment.url()
		alert_title = "Your comment has just been upvoted!"
		alert_message = ("Your comment on {0} just "
			"received a new upvote. Congrats! View your "
			"comment here: {1}").format(comment.post.title, url)

	elif alert_type == "POST-UPVOTE":
		post = Post.objects.get(pk=alert_obj_pk)		
		url = settings.HOST_NAME + post.full_url()
		alert_title = "Your post has just been upvoted!"
		alert_message = ("Your post: {0} just "
			"received a new upvote. Congrats! View your "
			"post here: {1}").format(post.title, url)

	elif alert_type == "POST-COMMENT":
		post = Post.objects.get(pk=alert_obj_pk)		
		url = settings.HOST_NAME + post.full_url()
		alert_title = "Your post has just received a new comment!"
		alert_message = ("Your post: {0} just "
			"received a new comment. Congrats! View your post "
			"and the new comment here: {1}").format(post.title, url)

	else:
		return

	subject, from_email = alert_title, settings.DEFAULT_FROM_EMAIL
	html = get_template('accounts/emails/alert-email.html')
	to = account.owner.email
	d = Context({'alert_title': alert_title, 'alert_message': alert_message})
	html_content = html.render(d)
	msg = EmailMultiAlternatives(subject, '<need to edit>', from_email, [to])
	msg.attach_alternative(html_content, 'text/html')
	msg.send()	