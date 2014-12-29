from django.contrib import admin

from posts.models import Post, PostRevision

class PostRevisionAdmin(admin.ModelAdmin):

	def approve(self, request, queryset):
		for revision in queryset:
			revision.approve()

	approve.short_description = "Approve the selected revisions"
	actions = ['approve']

admin.site.register(Post)
admin.site.register(PostRevision, PostRevisionAdmin)
