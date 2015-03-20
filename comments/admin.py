from django.contrib import admin

from comments.models import Comment

class CommentAdmin(admin.ModelAdmin):

	list_display = ['owner', 'created', 'vote_count', 'text']

admin.site.register(Comment, CommentAdmin)