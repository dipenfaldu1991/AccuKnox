from django.contrib import admin

# Register your models here.
from .models import UserData,FriendRequest

admin.site.register(UserData)
admin.site.register(FriendRequest)