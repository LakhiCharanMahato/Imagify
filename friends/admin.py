from django.contrib import admin
from .models import FriendList #, FriendRequest

# Register your models here.
class FriendListAdmin(admin.ModelAdmin):
    list_filter=['user1']
    list_display=['user1']
    searh_fields=['user1']
    readonly_fields=['user1','user2']

    class Meta:
        model=FriendList

admin.site.register(FriendList, FriendListAdmin)

# class FriendRequestAdmin(admin.ModelAdmin):
# list_filter=['sender','receiver']
# list_display=['sender','receiver']
# search_fields=['sender__username','sender__email','receiver__username','receiver__email']

# class Meta:
# model=FriendRequest

# admin.site.register(FriendRequest,FriendRequestAdmin)
