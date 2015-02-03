from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from celery import task

from accounts.models import Account
from posts.models import Post

@task()
def send_approved_email(account_pk, post_pk):
	account = Account.objects.get(pk=account_pk)
	post = Post.objects.get(pk=post_pk)

	subject = "Your submission \"{0}...\" has been approved".format(post.title[:18])
	from_email = settings.DEFAULT_FROM_EMAIL
	to = account.owner.email
	
	html = get_template('posts/emails/approved-email.html')
	context_dict = Context({'post': post, 'HOST_NAME': settings.HOST_NAME})
	html_content = html.render(context_dict)
	msg = EmailMultiAlternatives(subject, '<need to edit>', from_email, [to])
	msg.attach_alternative(html_content, 'text/html')
	msg.send()

@task()
def send_share_email(post_pk, sender, recipient):
	post = Post.objects.get(pk=post_pk)

	subject = "Check out \"{0}\" on Wikivinci".format(post.title)
	from_email = sender
	to = recipient
	message = ("I thought you might be interested in <a href=\"{0}\">\"{1}\"</a> "
		"on Wikivinci.<br /><br />This email was sent on http://www.Wikivinci.com. "
		"Learn faster from high quality, community curated tutorials and resources. "
	).format(settings.HOST_NAME+post.absolute_url(), post.title)

	send_mail(subject, message, from_email,
		[recipient], html_message=message,
		fail_silently=False,
	)

