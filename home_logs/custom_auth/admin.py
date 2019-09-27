from django.contrib import admin

from home_logs.custom_auth.models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    model = Token
    list_display = ('user', 'name', 'expired', 'invalid', 'expiration',)
