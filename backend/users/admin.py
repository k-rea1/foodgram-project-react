from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Follow

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    list_filter = ('first_name', 'email')
    empty_value_display = '---'
    
@admin.register(Follow)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'author', 'user'
    )
    list_filter = ('author', 'user')
    empy_value_display = '---'