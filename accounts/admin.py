from django.contrib import admin

from image_cropping import ImageCroppingMixin

from accounts.models import Account

class AccountAdmin(ImageCroppingMixin, admin.ModelAdmin):
    
    list_display = ['owner', 'points', 'can_comment', 'can_post', 'moderator']

admin.site.register(Account, AccountAdmin)