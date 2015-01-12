from django.contrib import admin

from posts.models import Post, PostRevision

class PostAdmin(admin.ModelAdmin):

	def get_queryset(self, request):
		qs = Post.incl_pending_posts
		ordering = self.get_ordering(request)
		if ordering:
			qs = qs.order_by(*ordering)
		return qs

	def approve(self, request, queryset):
		for post in queryset:
			if post.approved == False:
				post.approve()
	approve.short_description = "Approve the selected posts"
	actions = ['approve']

	list_display = ['title', 'approved']

class PostRevisionAdmin(admin.ModelAdmin):

	def approve(self, request, queryset):
		for revision in queryset:
			revision.approve()

	approve.short_description = "Approve the selected revisions"
	actions = ['approve']

admin.site.register(Post, PostAdmin)
admin.site.register(PostRevision, PostRevisionAdmin)
