from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone_number')
    search_fields = ('user__username', 'user__email', 'address', 'phone_number')
    list_filter = ('user',)
