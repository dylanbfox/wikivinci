from django.http import HttpResponseForbidden

def ajax_login_required(view):
	def wrapped_view(request, *args, **kwargs):
		if not request.user.is_authenticated():
			return HttpResponseForbidden()
		return view(request, *args, **kwargs)
	return wrapped_view