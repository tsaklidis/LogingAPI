from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from home_logs.accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # list_display = ['email', 'username',]
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('unlimited_tokens', 'persistent_tokens', 'allow_panel')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
